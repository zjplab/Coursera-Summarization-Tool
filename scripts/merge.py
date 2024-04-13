import os
import re
import sys

def format_heading(title, level):
    """Return a markdown heading based on title and level."""
    return f"{'#' * level} {title.replace('_', ' ').title()}\n\n"

def clean_srt_content(content):
    """Clean SRT file content, removing timestamps and line numbers."""
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.isdigit() or "-->" in line or line.strip() == '':
            continue
        else:
            new_lines.append(line)
    return '\n'.join(new_lines).strip() + '\n\n'

def natural_sort_key(s):
    """A key to sort strings with numeric parts in natural order."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def parse_course_input(course_or_url):
    """Extracts the course name from a URL or direct input."""
    match = re.search(r'/learn/([^/]+)', course_or_url)
    if match:
        return match.group(1)
    else:
        # Remove leading/trailing slashes and normalize
        return course_or_url.strip('/').replace('/', '-')

def create_transcript(course):
    # Determine the root directory and file names from the course parameter
    root_dir = f"./{course}/"
    output_file = f"./{course}.txt"
    main_heading = course.replace('-', ' ').title()

    formatted_content = format_heading(main_heading, 1)
    last_processed_dir = None  # Track the last processed directory path to avoid repetition

    for subdir, dirs, files in os.walk(root_dir):
        dirs.sort(key=natural_sort_key)
        files.sort(key=natural_sort_key)

        # Determine the heading level based on the directory depth
        heading_level = subdir.count(os.sep) - root_dir.count(os.sep) + 1
        subdir_title = os.path.basename(subdir).replace('_', ' ').title()

        # If we're in a new directory, add the directory heading
        if last_processed_dir != subdir:
            if subdir != root_dir:  # Skip the root directory itself
                formatted_content += format_heading(subdir_title, heading_level)
            last_processed_dir = subdir

        # Process each file within the directory
        for file in files:
            if file.endswith('.srt'):
                # Strip the .en.srt and any trailing numbering from the title
                section_title = re.sub(r'\.en\.srt$', '', file).replace('_', ' ').title()
                section_title = re.sub(r'\d+$', '', section_title).strip()

                # Add the file content as a subsection under the directory heading
                formatted_content += format_heading(section_title, heading_level + 1)
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as srt_file:
                    content = srt_file.read()
                    cleaned_content = clean_srt_content(content)
                    formatted_content += cleaned_content

    # Write the compiled content to the output file
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write(formatted_content)

    return f"Transcript has been written to {output_file}"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <course_name_or_url>")
        sys.exit(1)
    
    course_input = sys.argv[1]
    course_name = parse_course_input(course_input)
    message = create_transcript(course_name)
    print(message)
