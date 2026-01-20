import pymupdf as fitz 


def create_nup(input_pdf, output_pdf, n_cols=2, n_rows=2, orientation='portrait'):
    """Create n-up layout with specified orientation
    
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        n_cols: Number of columns per sheet (default: 2)
        n_rows: Number of rows per sheet (default: 2)
        orientation: 'portrait' or 'landscape' (default: 'portrait')
    """
    
    with fitz.open(input_pdf) as src:
        with fitz.open() as doc:
        
            pages_per_sheet = n_cols * n_rows
            margin = 20
            page_spacing = 10
            
            # Set page dimensions based on orientation (A4 size)
            if orientation.lower() == 'landscape':
                page_width_total = 842
                page_height_total = 595
            else:  # portrait
                page_width_total = 595
                page_height_total = 842
            
            src_rect = src[0].rect
            
            available_width = page_width_total - (2 * margin) - ((n_cols - 1) * page_spacing)
            available_height = page_height_total - (2 * margin) - ((n_rows - 1) * page_spacing)
            
            page_width = available_width / n_cols
            page_height = available_height / n_rows
            
            scale = min(page_width / src_rect.width, page_height / src_rect.height)
            scaled_width = src_rect.width * scale
            scaled_height = src_rect.height * scale
            
            for i in range(0, len(src), pages_per_sheet):
                new_page = doc.new_page(width=page_width_total, height=page_height_total)
                
                for row in range(n_rows):
                    for col in range(n_cols):
                        src_idx = i + (row * n_cols) + col
                        
                        if src_idx >= len(src):
                            break
                        
                        x = margin + col * (scaled_width + page_spacing)
                        y = margin + row * (scaled_height + page_spacing)
                        
                        target_rect = fitz.Rect(x, y, x + scaled_width, y + scaled_height)
                        
                        # Insert page
                        new_page.show_pdf_page(target_rect, src, src_idx)
            doc.save(output_pdf)
    

def merge_pdfs(input_pdfs, output_pdf):
    """Merge multiple PDFs into a single PDF
    
    Args:
        input_pdfs: List of PDF file paths in the order they should be merged.
                   The first PDF in the list will appear first in the output.
        output_pdf: Path to the output merged PDF file
    
    Example:
        merge_pdfs(['file1.pdf', 'file2.pdf', 'file3.pdf'], 'merged.pdf')
        # Result: file1 pages, then file2 pages, then file3 pages
    """
    with fitz.open() as doc:
    
        for input_pdf in input_pdfs:
            with fitz.open(input_pdf) as src:
                doc.insert_pdf(src)
        doc.save(output_pdf)
    

def split_pdf(input_pdf, output_folder, mode='pages', pages_per_split=1, page_ranges=None):
    """Split a PDF into multiple files
    
    Args:
        input_pdf: Path to input PDF file
        output_folder: Folder path where split PDFs will be saved
        mode: Split mode - 'pages' (individual pages), 'range' (custom ranges), or 'chunks' (every N pages)
        pages_per_split: Number of pages per split file (used when mode='chunks', default: 1)
        page_ranges: List of tuples for custom ranges (used when mode='range')
                    Example: [(0, 2), (3, 5), (6, 10)] for pages 1-3, 4-6, 7-11
    
    Examples:
        # Split into individual pages
        split_pdf('input.pdf', 'output/', mode='pages')
        
        # Split every 3 pages
        split_pdf('input.pdf', 'output/', mode='chunks', pages_per_split=3)
        
        # Split by custom ranges
        split_pdf('input.pdf', 'output/', mode='range', page_ranges=[(0, 2), (3, 5)])
    
    Returns:
        List of output file paths
    """
    import os
    
    output_files = []
    
    with fitz.open(input_pdf) as src:
        total_pages = len(src)
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        
        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)
        
        if mode == 'pages':
            # Split into individual pages
            for page_num in range(total_pages):
                with fitz.open() as output_doc:
                    output_doc.insert_pdf(src, from_page=page_num, to_page=page_num)
                    output_path = os.path.join(output_folder, f"{base_name}_page_{page_num + 1}.pdf")
                    output_doc.save(output_path)
                    output_files.append(output_path)
        
        elif mode == 'chunks':
            # Split every N pages
            chunk_num = 1
            for start_page in range(0, total_pages, pages_per_split):
                end_page = min(start_page + pages_per_split - 1, total_pages - 1)
                with fitz.open() as output_doc:
                    output_doc.insert_pdf(src, from_page=start_page, to_page=end_page)
                    output_path = os.path.join(output_folder, f"{base_name}_chunk_{chunk_num}.pdf")
                    output_doc.save(output_path)
                    output_files.append(output_path)
                    chunk_num += 1
        
        elif mode == 'range':
            # Split by custom ranges
            if not page_ranges:
                raise ValueError("page_ranges must be provided when mode='range'")
            
            for idx, (start, end) in enumerate(page_ranges, 1):
                if start < 0 or end >= total_pages:
                    raise ValueError(f"Invalid range ({start}, {end}). PDF has {total_pages} pages (0-{total_pages-1})")
                
                with fitz.open() as output_doc:
                    output_doc.insert_pdf(src, from_page=start, to_page=end)
                    output_path = os.path.join(output_folder, f"{base_name}_range_{idx}.pdf")
                    output_doc.save(output_path)
                    output_files.append(output_path)
        
        else:
            raise ValueError(f"Invalid mode '{mode}'. Must be 'pages', 'chunks', or 'range'")
    
    return output_files


def delete_pages(input_pdf, output_pdf, pages_to_delete):
    """Delete specific pages from a PDF
    
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        pages_to_delete: List of page numbers to delete (1-based indexing)
                        Example: [1, 3, 5] to delete pages 1, 3, and 5
    
    Example:
        delete_pages('input.pdf', 'output.pdf', [1, 3, 5])
    """
    with fitz.open(input_pdf) as doc:
        # Convert to 0-based indexing and sort in reverse to delete from end
        pages_to_delete_sorted = sorted([p - 1 for p in pages_to_delete], reverse=True)
        
        # Validate page numbers
        for page_num in pages_to_delete_sorted:
            if page_num < 0 or page_num >= len(doc):
                raise ValueError(f"Invalid page number: {page_num + 1}. PDF has {len(doc)} pages")
        
        # Delete pages from end to start to avoid index shifting issues
        for page_num in pages_to_delete_sorted:
            doc.delete_page(page_num)
        
        doc.save(output_pdf)


def rotate_pages(input_pdf, output_pdf, rotation, pages='all'):
    """Rotate pages in a PDF
    
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        rotation: Rotation angle in degrees (90, 180, 270, or -90, -180, -270)
        pages: Pages to rotate - 'all', list of page numbers (1-based), or 'even'/'odd'
               Example: [1, 3, 5] or 'all' or 'even' or 'odd'
    
    Examples:
        rotate_pages('input.pdf', 'output.pdf', 90, pages='all')
        rotate_pages('input.pdf', 'output.pdf', 180, pages=[1, 2, 3])
        rotate_pages('input.pdf', 'output.pdf', 90, pages='even')
    """
    if rotation not in [90, 180, 270, -90, -180, -270]:
        raise ValueError("Rotation must be 90, 180, 270, -90, -180, or -270 degrees")
    
    with fitz.open(input_pdf) as doc:
        total_pages = len(doc)
        
        # Determine which pages to rotate
        if pages == 'all':
            pages_to_rotate = list(range(total_pages))
        elif pages == 'even':
            pages_to_rotate = [i for i in range(total_pages) if (i + 1) % 2 == 0]
        elif pages == 'odd':
            pages_to_rotate = [i for i in range(total_pages) if (i + 1) % 2 == 1]
        else:
            # Convert 1-based to 0-based indexing
            pages_to_rotate = [p - 1 for p in pages]
            
            # Validate page numbers
            for page_num in pages_to_rotate:
                if page_num < 0 or page_num >= total_pages:
                    raise ValueError(f"Invalid page number: {page_num + 1}. PDF has {total_pages} pages")
        
        # Rotate the specified pages
        for page_num in pages_to_rotate:
            page = doc[page_num]
            page.set_rotation(rotation)
        
        doc.save(output_pdf)


def compress_pdf(input_pdf, output_pdf, compression_level='medium'):
    """Compress a PDF to reduce file size
    
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        compression_level: 'low', 'medium', or 'high' (default: 'medium')
                          - low: minimal compression, best quality
                          - medium: balanced compression and quality
                          - high: maximum compression, lower quality
    
    Example:
        compress_pdf('input.pdf', 'output.pdf', compression_level='high')
    """
    compression_settings = {
        'low': {
            'garbage': 1,
            'deflate': True,
            'deflate_images': False,
            'deflate_fonts': False,
        },
        'medium': {
            'garbage': 3,
            'deflate': True,
            'deflate_images': True,
            'deflate_fonts': True,
        },
        'high': {
            'garbage': 4,
            'deflate': True,
            'deflate_images': True,
            'deflate_fonts': True,
            'clean': True,
        }
    }
    
    if compression_level not in compression_settings:
        raise ValueError("compression_level must be 'low', 'medium', or 'high'")
    
    settings = compression_settings[compression_level]
    
    with fitz.open(input_pdf) as doc:
        doc.save(output_pdf, **settings)


def word_to_pdf(input_docx, output_pdf):
    """Convert Microsoft Word document to PDF
    
    Args:
        input_docx: Path to input Word file (.doc or .docx)
        output_pdf: Path to output PDF file
    
    Note:
        Requires Microsoft Word to be installed on Windows.
        Uses win32com to automate Word conversion.
    
    Example:
        word_to_pdf('document.docx', 'document.pdf')
    """
    import os
    import win32com.client
    
    # Convert to absolute paths
    input_docx = os.path.abspath(input_docx)
    output_pdf = os.path.abspath(output_pdf)
    
    # Create Word application object
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    try:
        # Open the document
        doc = word.Documents.Open(input_docx)
        
        # Save as PDF (format 17 is PDF)
        doc.SaveAs(output_pdf, FileFormat=17)
        
        # Close the document
        doc.Close()
    finally:
        # Quit Word
        word.Quit()


def powerpoint_to_pdf(input_pptx, output_pdf):
    """Convert Microsoft PowerPoint presentation to PDF
    
    Args:
        input_pptx: Path to input PowerPoint file (.ppt or .pptx)
        output_pdf: Path to output PDF file
    
    Note:
        Requires Microsoft PowerPoint to be installed on Windows.
        Uses win32com to automate PowerPoint conversion.
    
    Example:
        powerpoint_to_pdf('presentation.pptx', 'presentation.pdf')
    """
    import os
    import win32com.client
    
    # Convert to absolute paths
    input_pptx = os.path.abspath(input_pptx)
    output_pdf = os.path.abspath(output_pdf)
    
    # Create PowerPoint application object
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1
    
    try:
        # Open the presentation
        presentation = powerpoint.Presentations.Open(input_pptx, WithWindow=False)
        
        # Save as PDF (format 32 is PDF)
        presentation.SaveAs(output_pdf, FileFormat=32)
        
        # Close the presentation
        presentation.Close()
    finally:
        # Quit PowerPoint
        powerpoint.Quit()


def add_watermark(input_pdf, output_pdf, watermark_text, opacity=0.3, font_size=50, 
                  color=(0.5, 0.5, 0.5), rotation=45, position='center'):
    """Add watermark text to all pages of a PDF
    
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        watermark_text: Text to use as watermark
        opacity: Watermark opacity (0.0 to 1.0, default: 0.3)
        font_size: Font size for watermark (default: 50)
        color: RGB color tuple (0.0 to 1.0 for each component, default: (0.5, 0.5, 0.5))
        rotation: Rotation angle in degrees (default: 45). 
                  For best results use 0, 45, 90, 135, 180, 225, 270, 315
        position: Position of watermark - 'center', 'top', 'bottom' (default: 'center')
    
    Example:
        add_watermark('input.pdf', 'output.pdf', 'CONFIDENTIAL', opacity=0.2)
        add_watermark('input.pdf', 'output.pdf', 'DRAFT', font_size=60, color=(1, 0, 0))
    """
    import math
    
    with fitz.open(input_pdf) as doc:
        for page in doc:
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height
            
            # Determine watermark center position based on position parameter
            center_x = page_width / 2
            if position == 'top':
                center_y = page_height * 0.25
            elif position == 'bottom':
                center_y = page_height * 0.75
            else:  # center (default)
                center_y = page_height / 2
            
            # Create a temporary TextWriter to measure text dimensions
            temp_tw = fitz.TextWriter(page_rect)
            temp_tw.append(fitz.Point(0, 0), watermark_text, fontsize=font_size)
            text_rect = temp_tw.text_rect
            text_width = text_rect.width
            text_height = text_rect.height
            
            # Create the actual TextWriter
            tw = fitz.TextWriter(page_rect)
            
            # Calculate text position so it's centered at (center_x, center_y)
            # Text is drawn from baseline, so we offset accordingly
            text_start_x = center_x - text_width / 2
            text_start_y = center_y + text_height / 4  # Approximate vertical centering
            
            # Add the watermark text
            tw.append(
                fitz.Point(text_start_x, text_start_y),
                watermark_text,
                fontsize=font_size
            )
            
            # Apply rotation if specified
            if rotation != 0:
                # Convert degrees to radians
                angle_rad = math.radians(rotation)
                cos_a = math.cos(angle_rad)
                sin_a = math.sin(angle_rad)
                
                # Create rotation matrix
                rotation_matrix = fitz.Matrix(cos_a, sin_a, -sin_a, cos_a, 0, 0)
                
                # Pivot point is the center of the page (where watermark is centered)
                pivot = fitz.Point(center_x, center_y)
                
                # Write text with rotation and opacity
                tw.write_text(
                    page,
                    opacity=opacity,
                    color=color,
                    morph=(pivot, rotation_matrix),
                    overlay=True
                )
            else:
                # No rotation - just write with opacity
                tw.write_text(
                    page,
                    opacity=opacity,
                    color=color,
                    overlay=True
                )
        
        doc.save(output_pdf)


def add_page_numbers(input_pdf, output_pdf, position='bottom-right', 
                     font_size=10, color=(0, 0, 0), format_string='{page}',
                     start_number=1, pages='all'):
    """Add page numbers to a PDF
    
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        position: Position of page numbers - 'top-left', 'top-center', 'top-right',
                 'bottom-left', 'bottom-center', 'bottom-right' (default: 'bottom-right')
        font_size: Font size for page numbers (default: 10)
        color: RGB color tuple (0.0 to 1.0 for each component, default: (0, 0, 0))
        format_string: Format string for page numbers (default: '{page}')
                      Available placeholders: {page}, {total}
                      Examples: '{page}', 'Page {page}', '{page} of {total}'
        start_number: Starting page number (default: 1)
        pages: Pages to number - 'all', list of page numbers (1-based)
               Example: [1, 3, 5] or 'all'
    
    Examples:
        add_page_numbers('input.pdf', 'output.pdf')
        add_page_numbers('input.pdf', 'output.pdf', position='bottom-center', 
                        format_string='Page {page} of {total}')
        add_page_numbers('input.pdf', 'output.pdf', pages=[2, 3, 4], start_number=1)
    """
    with fitz.open(input_pdf) as doc:
        total_pages = len(doc)
        margin = 30
        
        # Determine which pages to number
        if pages == 'all':
            pages_to_number = list(range(total_pages))
        else:
            # Convert 1-based to 0-based indexing
            pages_to_number = [p - 1 for p in pages]
            
            # Validate page numbers
            for page_num in pages_to_number:
                if page_num < 0 or page_num >= total_pages:
                    raise ValueError(f"Invalid page number: {page_num + 1}. PDF has {total_pages} pages")
        
        for idx, page_num in enumerate(pages_to_number):
            page = doc[page_num]
            page_rect = page.rect
            
            # Calculate current page number
            current_page_num = start_number + idx
            
            # Format the page number text
            page_text = format_string.format(page=current_page_num, total=len(pages_to_number))
            
            # Calculate position
            if position == 'bottom-right':
                point = fitz.Point(page_rect.width - margin, page_rect.height - margin)
            elif position == 'bottom-center':
                point = fitz.Point(page_rect.width / 2, page_rect.height - margin)
            elif position == 'bottom-left':
                point = fitz.Point(margin, page_rect.height - margin)
            elif position == 'top-right':
                point = fitz.Point(page_rect.width - margin, margin)
            elif position == 'top-center':
                point = fitz.Point(page_rect.width / 2, margin)
            elif position == 'top-left':
                point = fitz.Point(margin, margin)
            else:
                raise ValueError(f"Invalid position: {position}")
            
            # Add the page number
            page.insert_text(point, page_text, fontsize=font_size, color=color)
        
        doc.save(output_pdf)

