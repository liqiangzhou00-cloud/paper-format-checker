rules:
  - rule_id: COVER_TITLE_ALIGNMENT
    rule_type: section
    title: Title should be centered and formatted as a 3-level title
    severity: error
    description: Chinese title should be centered, with bold black font and consistent formatting.
    location: cover
    suggestion: Use centered 3-level black body title and keep it consistent with other materials.

  - rule_id: COVER_TITLE_CONSISTENT
    rule_type: structural
    title: Title must match across all materials
    severity: error
    description: The title must be identical across the cover, abstract, and supporting documents.
    location: metadata
    suggestion: Ensure all title strings are exactly the same including punctuation and spacing.

  - rule_id: ABSTRACT_LENGTH
    rule_type: prose
    title: Abstract length should be within 500-800 Chinese characters
    severity: warning
    description: Abstract length should be between 500 and 800 characters and written in a concise format.
    location: abstract
    suggestion: Ensure the abstract includes purpose, method, result, and conclusion while staying within the required length.

  - rule_id: CHAPTER_SEPARATOR
    rule_type: structure
    title: Each chapter should begin on a new page
    severity: error
    description: New chapters should begin on a new page.
    location: section
    suggestion: Insert page breaks before each chapter heading.

  - rule_id: SECTION_LEVELING
    rule_type: structure
    title: Section hierarchy must follow levels 1, 2, 3
    severity: warning
    description: Chapter titles, section titles, and subsection titles should use a clear hierarchy.
    location: section
    suggestion: Keep an ordered outline with level 1, 2, and 3 headings only.

  - rule_id: CHAPTER_SUMMARY
    rule_type: structure
    title: Summary should appear after each chapter from chapter 2 onward
    severity: warning
    description: Chapters after the first should include a brief summary paragraph.
    location: section
    suggestion: Add a '本章小结' section at the end of each chapter.

  - rule_id: FIGURE_CAPTION_FORMAT
    rule_type: figure
    title: Figure captions must be placed below the figure
    severity: error
    description: Each figure requires a caption below the image, with the correct numbering format.
    location: figure
    suggestion: Use a format like '图2-1' and place the caption beneath the image.

  - rule_id: TABLE_CAPTION_FORMAT
    rule_type: table
    title: Table captions must be placed above the table
    severity: error
    description: Each table must have a caption above it, following the section-numbered format.
    location: table
    suggestion: Use a format like '表3-1' and place the caption on top of the table.

  - rule_id: REFERENCE_SEQUENCE
    rule_type: reference
    title: Reference numbering must start at 1 and be sequential
    severity: error
    description: Citation markers must begin at [1] and follow the text order exactly.
    location: references
    suggestion: Ensure each reference is cited in ascending order and without gaps.

  - rule_id: REFERENCE_MIN_COUNT
    rule_type: reference
    title: Minimum reference count is required
    severity: warning
    description: The paper should include a sufficient number of cited references.
    location: references
    suggestion: Use at least 15 references, including a meaningful number of recent and external works.

  - rule_id: ACKNOWLEDGEMENT_SECTION
    rule_type: section
    title: Acknowledgements section must be in the correct position
    severity: warning
    description: Acknowledgements should be after the references and formatted as a dedicated section.
    location: acknowledgement
    suggestion: Insert a separate acknowledgements section after the references.

  - rule_id: APPENDIX_FORMAT
    rule_type: appendix
    title: Appendix should be separate and optional
    severity: info
    description: Appendix is optional and should be separated from the main text when applicable.
    location: appendix
    suggestion: If used, label appendices clearly such as '附录1'.
