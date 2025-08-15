import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os
import io
import base64
from pdf2image import convert_from_path
import tempfile
import re
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Bank Check Extractor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_image(image):
    """Extract text from an image using OCR"""
    try:
        # Convert PIL image to numpy array for OpenCV processing
        img_array = np.array(image)
        
        # Preprocessing for better OCR results
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply threshold to get image with only black and white
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Noise removal
        kernel = np.ones((1,1), np.uint8)
        processed_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        processed_img = cv2.medianBlur(processed_img, 3)
        
        # Convert back to PIL Image
        processed_pil = Image.fromarray(processed_img)
        
        # Extract text
        text = pytesseract.image_to_string(processed_pil, config='--psm 6')
        return text, processed_pil
    except Exception as e:
        st.error(f"Error in OCR processing: {str(e)}")
        return "", image

def parse_check_data(text):
    """Parse extracted text to find check information"""
    data = {
        "Date": "Not found",
        "Account Number": "Not found", 
        "Check Number": "Not found",
        "Amount (Numbers)": "Not found",
        "Amount (Words)": "Not found",
        "Pay to": "Not found",
        "Bank Name": "Not found",
        "Routing Number": "Not found"
    }
    
    lines = text.split('\n')
    text_upper = text.upper()
    
    # Date patterns
    date_patterns = [
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',
        r'\b((?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[A-Z]*\s+\d{1,2},?\s+\d{4})\b'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["Date"] = match.group(1)
            break
    
    # Account number (usually longer sequence of digits)
    account_pattern = r'\b(\d{10,})\b'
    account_matches = re.findall(account_pattern, text)
    if account_matches:
        # Usually the longest number is the account number
        data["Account Number"] = max(account_matches, key=len)
    
    # Check number (usually shorter sequence)
    check_pattern = r'(?:CHECK|CHK|#)\s*(\d+)'
    check_match = re.search(check_pattern, text_upper)
    if check_match:
        data["Check Number"] = check_match.group(1)
    
    # Amount in numbers
    amount_pattern = r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
    amount_match = re.search(amount_pattern, text)
    if amount_match:
        data["Amount (Numbers)"] = amount_match.group(1)
    
    # Amount in words (look for lines with monetary words)
    money_words = ['DOLLAR', 'CENT', 'HUNDRED', 'THOUSAND', 'MILLION']
    for line in lines:
        line_upper = line.upper()
        if any(word in line_upper for word in money_words) and len(line.strip()) > 10:
            data["Amount (Words)"] = line.strip()
            break
    
    # Pay to (look for "PAY TO" or similar)
    pay_patterns = [
        r'PAY\s+TO[:\s]+(.+?)(?:\n|$)',
        r'PAY\s+TO\s+THE\s+ORDER\s+OF[:\s]+(.+?)(?:\n|$)'
    ]
    
    for pattern in pay_patterns:
        match = re.search(pattern, text_upper)
        if match:
            data["Pay to"] = match.group(1).strip()
            break
    
    # Routing number (9 digits, often at bottom)
    routing_pattern = r'\b([0-9]{9})\b'
    routing_matches = re.findall(routing_pattern, text)
    if routing_matches:
        data["Routing Number"] = routing_matches[0]
    
    return data

def pdf_to_images(pdf_file):
    """Convert PDF to images"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.read())
            tmp_file_path = tmp_file.name
        
        images = convert_from_path(tmp_file_path)
        os.unlink(tmp_file_path)  # Clean up temp file
        return images
    except Exception as e:
        st.error(f"Error converting PDF: {str(e)}")
        return []

def main():
    # Header
    st.markdown('<h1 class="main-header">🏦 Bank Check Extractor Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        page = st.selectbox("Choose a page", ["Home", "Upload & Process", "Batch Processing", "Analytics"])
        
        st.markdown("### ⚙️ Settings")
        confidence_threshold = st.slider("OCR Confidence Threshold", 0, 100, 70)
        preprocessing = st.checkbox("Enable Image Preprocessing", value=True)
        
        st.markdown("### 📊 Quick Stats")
        if 'processed_checks' not in st.session_state:
            st.session_state.processed_checks = 0
        if 'total_amount' not in st.session_state:
            st.session_state.total_amount = 0.0
            
        st.metric("Checks Processed", st.session_state.processed_checks)
        st.metric("Total Amount", f"${st.session_state.total_amount:,.2f}")

    if page == "Home":
        st.markdown("### Welcome to the Bank Check Extractor!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🔍 OCR Technology</h3>
                <p>Advanced text recognition using Tesseract OCR with image preprocessing</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📄 PDF Support</h3>
                <p>Process individual PDFs or batch upload multiple check files</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Data Export</h3>
                <p>Export extracted data to CSV, Excel, or JSON formats</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Getting Started")
        st.write("""
        1. **Upload**: Go to 'Upload & Process' to upload your check PDF or image
        2. **Extract**: Our OCR engine will automatically extract text and data
        3. **Review**: Verify the extracted information and make corrections if needed
        4. **Export**: Download the processed data in your preferred format
        """)
        
        # Sample data visualization
        st.markdown("### 📈 Sample Processing Results")
        sample_data = pd.DataFrame({
            'Check Number': ['1001', '1002', '1003', '1004'],
            'Date': ['01/15/2024', '01/16/2024', '01/17/2024', '01/18/2024'],
            'Amount': [250.00, 1500.75, 89.99, 3200.00],
            'Status': ['Processed', 'Processed', 'Processed', 'Processed']
        })
        st.dataframe(sample_data, use_container_width=True)

    elif page == "Upload & Process":
        st.markdown('<h2 class="sub-header">📤 Upload and Process Checks</h2>', unsafe_allow_html=True)
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=['pdf', 'png', 'jpg', 'jpeg'],
            help="Upload a PDF containing check images or individual check images"
        )
        
        if uploaded_file is not None:
            file_type = uploaded_file.type
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 📄 Original File")
                
                if file_type == "application/pdf":
                    st.write("📋 PDF File uploaded")
                    with st.spinner("Converting PDF to images..."):
                        images = pdf_to_images(uploaded_file)
                    
                    if images:
                        st.success(f"✅ Converted to {len(images)} image(s)")
                        image_to_process = images[0]  # Process first page
                        st.image(image_to_process, caption="First page", use_container_width=True)
                else:
                    image_to_process = Image.open(uploaded_file)
                    st.image(image_to_process, caption="Uploaded Image", use_container_width=True)
            
            with col2:
                st.markdown("### 🔍 Processing Results")
                
                if st.button("🚀 Extract Data", type="primary"):
                    with st.spinner("Extracting text from image..."):
                        extracted_text, processed_img = extract_text_from_image(image_to_process)
                    
                    if extracted_text:
                        # Parse the data
                        parsed_data = parse_check_data(extracted_text)
                        
                        st.markdown("#### 📊 Extracted Information")
                        
                        # Display results in a nice format
                        for key, value in parsed_data.items():
                            if value != "Not found":
                                st.success(f"**{key}**: {value}")
                            else:
                                st.warning(f"**{key}**: {value}")
                        
                        # Show processed image
                        with st.expander("🖼️ View Processed Image"):
                            st.image(processed_img, caption="Processed Image", use_container_width=True)
                        
                        # Show raw text
                        with st.expander("📝 View Raw Extracted Text"):
                            st.text_area("Raw OCR Text", extracted_text, height=200)
                        
                        # Update session state
                        st.session_state.processed_checks += 1
                        if parsed_data["Amount (Numbers)"] != "Not found":
                            try:
                                amount = float(parsed_data["Amount (Numbers)"].replace(',', ''))
                                st.session_state.total_amount += amount
                            except:
                                pass
                        
                        # Export options
                        st.markdown("#### 💾 Export Data")
                        col_csv, col_json = st.columns(2)
                        
                        with col_csv:
                            df = pd.DataFrame([parsed_data])
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download CSV",
                                data=csv,
                                file_name=f"check_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime='text/csv'
                            )
                        
                        with col_json:
                            import json
                            json_data = json.dumps(parsed_data, indent=2)
                            st.download_button(
                                label="📥 Download JSON",
                                data=json_data,
                                file_name=f"check_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime='application/json'
                            )
                    else:
                        st.error("❌ Could not extract text from the image. Please try with a clearer image.")

    elif page == "Batch Processing":
        st.markdown('<h2 class="sub-header">📚 Batch Processing</h2>', unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Choose multiple files", 
            type=['pdf', 'png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload multiple check files for batch processing"
        )
        
        if uploaded_files:
            st.write(f"📁 {len(uploaded_files)} files uploaded")
            
            if st.button("🔄 Process All Files", type="primary"):
                progress_bar = st.progress(0)
                results = []
                
                for i, file in enumerate(uploaded_files):
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    
                    try:
                        if file.type == "application/pdf":
                            images = pdf_to_images(file)
                            if images:
                                image = images[0]
                            else:
                                continue
                        else:
                            image = Image.open(file)
                        
                        extracted_text, _ = extract_text_from_image(image)
                        parsed_data = parse_check_data(extracted_text)
                        parsed_data['Filename'] = file.name
                        results.append(parsed_data)
                        
                    except Exception as e:
                        st.error(f"Error processing {file.name}: {str(e)}")
                
                if results:
                    st.success(f"✅ Processed {len(results)} files successfully!")
                    
                    # Display results
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                    
                    # Export all results
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download All Results (CSV)",
                        data=csv,
                        file_name=f"batch_check_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime='text/csv'
                    )

    elif page == "Analytics":
        st.markdown('<h2 class="sub-header">📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
        
        # Sample analytics (in a real app, this would be from a database)
        st.info("📌 This is a demo analytics page. In a production environment, this would show real processing statistics.")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Checks", "1,247", "+12%")
        with col2:
            st.metric("Success Rate", "94.2%", "+2.1%")
        with col3:
            st.metric("Avg Process Time", "2.3s", "-0.5s")
        with col4:
            st.metric("Total Amount", "$2.4M", "+8.3%")
        
        # Charts
        chart_data = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'Checks Processed': np.random.randint(20, 100, 30),
            'Success Rate': np.random.uniform(0.85, 0.98, 30)
        })
        
        st.line_chart(chart_data.set_index('Date'))

if __name__ == "__main__":
    main()
