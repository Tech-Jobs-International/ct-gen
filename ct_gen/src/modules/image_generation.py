import streamlit as st
import markdown
import imgkit
import os
from io import BytesIO
import streamlit
from weasyprint import HTML
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfFileReader, PdfFileWriter


# Function to convert markdown to image
# def markdown_to_image(md_text):
#     html_text = markdown.markdown(md_text)
#     styled_html = f"<html><head><style>body {{ font-family: Arial; }}</style></head><body>{html_text}</body></html>"
    
#     # Convert HTML to an image
#     img = imgkit.from_string(styled_html, False)
#     return img

def markdown_to_image(md_text):
    # Convert markdown text to HTML
    html_text = markdown.markdown(md_text)

    # Convert HTML to an image using WeasyPrint
    html = HTML(string=html_text)
    img = html.write_png()

    return img


def markdown_to_pdf(md_text):
    # Convert markdown text to HTML
    html_text = markdown.markdown(md_text)

    # Convert HTML to a PDF using WeasyPrint
    html = HTML(string=html_text)
    pdf = html.write_pdf()

    return pdf

def add_watermark_to_pdf(input_pdf, watermark_text):
    # Open the PDF
    pdf = fitz.open(stream=input_pdf)

    for page in pdf:
        # Define font size and color for the watermark
        font_size = 15  # Adjust size as needed
        color = (0.6, 0.6, 0.6)  # grey color

        # Calculate the position for the watermark, centered and rotated
        text_width, text_height = page.get_text_size(watermark_text, fontsize=font_size)
        x_pos = (page.rect.width - text_width) / 2
        y_pos = (page.rect.height + text_height) / 2

        # Create a text rotation matrix (45 degrees rotation)
        rotate = fitz.Matrix(45, 45)

        # Insert watermark text with rotation
        page.insert_text(
            (x_pos, y_pos),  # position
            watermark_text,  # text
            fontsize=font_size,  # font size
            rotate=rotate,  # rotation
            color=color  # text color
        )

    # Save the watermarked PDF to a bytes buffer
    out_buffer = BytesIO()
    pdf.save(out_buffer)
    pdf.close()
    return out_buffer.getvalue()


def make_watermark(pdf, text):
    pdf.translate(inch, inch)
    pdf.setFillColor(colors.grey, alpha=0.6)
    pdf.setFont("Helvetica", 50)
    pdf.rotate(45)
    pdf.drawCentredString(400, 100, text)
    return pdf


def create_img_download_button(text):
    # Button to convert markdown to image
    # if st.button('Download as Image'):
    #     with st.spinner('Converting...'):
    #         img = markdown_to_pdf(text)

    #         # Convert the image for download
    #         if img:
    #             st.success("Conversion Successful!")
    #             btn = st.download_button(
    #                 label="Download Image",
    #                 data=BytesIO(img),
    #                 file_name="markdown_image.jpg",
    #                 mime="image/jpeg"
    #             )
    #         else:
    #             st.error("Conversion Failed!")

    if st.button('Convert'):
            with st.spinner('Converting...'):
                pdf = markdown_to_pdf(text)
                #pdf = add_watermark_to_pdf(pdf, "Conspiracy Theory")
                pdf = make_watermark(pdf, "Conspiracy Theory")

                # Convert the PDF for download
                if pdf:
                    st.success("Conversion Successful!")
                    st.download_button(
                        label="Download PDF",
                        data=BytesIO(pdf),
                        file_name="markdown_document.pdf",
                        mime="application/octet-stream"
                    )
                else:
                    st.error("Conversion Failed!")
