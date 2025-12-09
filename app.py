import streamlit as st
import fitz
import io
import zipfile
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="PDF Image Extractor",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
    }
    .image-container {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def extract_images(pdf_bytes, progress_bar=None):
    """Extract images from PDF with progress tracking"""
    try:
        pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
        extracted_files = []
        total_pages = len(pdf)

        for page_num in range(total_pages):
            if progress_bar:
                progress_bar.progress((page_num + 1) / total_pages)
            
            page = pdf[page_num]
            images = page.get_images(full=True)

            for img_index, img in enumerate(images, start=1):
                try:
                    xref = img[0]
                    base_image = pdf.extract_image(xref)

                    img_bytes = base_image["image"]
                    img_ext = base_image["ext"]
                    filename = f"image_p{page_num+1}_i{img_index}.{img_ext}"

                    extracted_files.append({
                        "filename": filename,
                        "bytes": img_bytes,
                        "page": page_num + 1,
                        "index": img_index,
                        "ext": img_ext
                    })
                except Exception as e:
                    st.warning(f"Failed to extract image on page {page_num+1}: {str(e)}")
                    continue

        pdf.close()
        return extracted_files
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return []

def convert_image_format(img_bytes, target_format, quality=85):
    """Convert image to target format"""
    try:
        img = Image.open(io.BytesIO(img_bytes))
        output = io.BytesIO()
        
        if target_format.upper() in ["JPG", "JPEG"]:
            img.save(output, format="JPEG", quality=quality)
        elif target_format.upper() == "WEBP":
            img.save(output, format="WEBP", quality=quality)
        else:
            img.save(output, format=target_format.upper())
        
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.warning(f"Could not convert image: {str(e)}")
        return img_bytes

def create_zip_file(images):
    """Create ZIP file with all images"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for img in images:
            zipf.writestr(img["filename"], img["bytes"])
    zip_buffer.seek(0)
    return zip_buffer

# Initialize session state
if "extracted_images" not in st.session_state:
    st.session_state.extracted_images = []

# Main UI
st.title("🖼️ PDF Image Extractor Pro")
st.write("Extract, preview, and download images from PDF files with advanced options.")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    output_format = st.selectbox(
        "Output Format",
        ["Original", "PNG", "JPG", "WEBP"],
        help="Convert images to a specific format"
    )
    
    quality = st.slider(
        "Image Quality (for JPG/WEBP)",
        min_value=50,
        max_value=100,
        value=85,
        step=5
    )
    
    st.divider()
    st.info("📌 Upload a PDF to get started!")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

with col2:
    if uploaded_file:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.metric("File Size", f"{file_size_mb:.2f} MB")

if uploaded_file:
    pdf_bytes = uploaded_file.read()
    
    # Extract button
    if st.button("🔍 Extract Images", use_container_width=True, type="primary"):
        progress_bar = st.progress(0)
        
        with st.spinner("Extracting images from PDF..."):
            st.session_state.extracted_images = extract_images(pdf_bytes, progress_bar)
        
        progress_bar.empty()
        
        if st.session_state.extracted_images:
            st.success(f"✅ Successfully extracted {len(st.session_state.extracted_images)} images!")
        else:
            st.warning("⚠️ No images found in this PDF.")
    
    # Display extracted images
    if st.session_state.extracted_images:
        st.divider()
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📸 Preview", "📋 Details", "⬇️ Download"])
        
        with tab1:
            st.subheader("Image Preview")
            
            # Create columns for image grid
            cols_per_row = st.slider("Images per row", 1, 5, 3)
            cols = st.columns(cols_per_row)
            
            for idx, img_data in enumerate(st.session_state.extracted_images):
                col = cols[idx % cols_per_row]
                
                with col:
                    try:
                        img = Image.open(io.BytesIO(img_data["bytes"]))
                        st.image(
                            img,
                            caption=f"Page {img_data['page']}, Image {img_data['index']}",
                            use_column_width=True
                        )
                    except Exception as e:
                        st.error(f"Could not display image: {str(e)}")
        
        with tab2:
            st.subheader("Image Details")
            
            # Create a summary table
            summary_data = []
            for idx, img_data in enumerate(st.session_state.extracted_images):
                summary_data.append({
                    "Index": idx,
                    "Filename": img_data["filename"],
                    "Page": img_data["page"],
                    "Format": img_data["ext"].upper(),
                    "Size (KB)": round(len(img_data["bytes"]) / 1024, 2)
                })
            
            st.dataframe(summary_data, use_container_width=True)
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Images", len(st.session_state.extracted_images))
            with col2:
                total_size = sum(len(img["bytes"]) for img in st.session_state.extracted_images) / (1024 * 1024)
                st.metric("Total Size", f"{total_size:.2f} MB")
            with col3:
                pages_with_images = len(set(img["page"] for img in st.session_state.extracted_images))
                st.metric("Pages with Images", pages_with_images)
        
        with tab3:
            st.subheader("Download Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Download as ZIP**")
                
                # Prepare images for download
                images_to_download = st.session_state.extracted_images
                
                # Apply format conversion if needed
                processed_images = []
                for img_data in images_to_download:
                    img_copy = img_data.copy()
                    
                    if output_format != "Original":
                        img_copy["bytes"] = convert_image_format(
                            img_data["bytes"],
                            output_format,
                            quality
                        )
                        img_copy["filename"] = img_copy["filename"].rsplit(".", 1)[0] + f".{output_format.lower()}"
                    
                    processed_images.append(img_copy)
                
                zip_buffer = create_zip_file(processed_images)
                
                st.download_button(
                    label=f"⬇️ Download ZIP ({len(processed_images)} images)",
                    data=zip_buffer,
                    file_name="extracted_images.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            
            with col2:
                st.write("**Individual Downloads**")
                st.write("Download specific images individually:")
                
                for idx, img_data in enumerate(st.session_state.extracted_images):
                    img_bytes = img_data["bytes"]
                    
                    if output_format != "Original":
                        img_bytes = convert_image_format(img_bytes, output_format, quality)
                        filename = img_data["filename"].rsplit(".", 1)[0] + f".{output_format.lower()}"
                    else:
                        filename = img_data["filename"]
                    
                    st.download_button(
                        label=f"📥 {filename}",
                        data=img_bytes,
                        file_name=filename,
                        key=f"download_{idx}",
                        use_container_width=True
                    )
        
        st.divider()
        st.info("💡 **Tips:** Use the Preview tab to view all images, check Details for statistics, and use Download for batch or individual downloads!")

else:
    st.info("👆 Start by uploading a PDF file above!")
