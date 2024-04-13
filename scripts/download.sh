#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <course_or_url> <cauth>"
    exit 1
fi

# Assign the first argument to 'course_or_url' and the second to 'cauth'
course_or_url="$1"
cauth="$2"

# Extract course name from URL if necessary
if [[ $course_or_url =~ /learn/([^/]+) ]]; then
    course="${BASH_REMATCH[1]}"
else
    course="$course_or_url"  # use the input directly if it doesn't match expected URL format
fi

# Clone the repository
git clone https://github.com/raffaem/cs-dlp
cd cs-dlp

# Install the required Python package locally
python -m pip install --user .

# Navigate back to the parent directory
cd ..

# Run the cs-dlp command with the specified options
/root/.local/bin/cs-dlp "$course" -f "pdf srt" --subtitle-language en --ignore-formats "mp4 webm" --cauth "$cauth"
