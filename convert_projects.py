#!/usr/bin/env python3
"""
Convert Projects.tsv to a searchable index.md page for MkDocs.
Excludes: Id, Start time, Completion time
"""

import csv
from pathlib import Path


def convert_tsv_to_markdown(tsv_path: Path, output_path: Path):
    """Convert TSV file to searchable Markdown format with improved markup."""

    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        projects = list(reader)
    
    # Fields to exclude or handle specially
    exclude_fields = {
        'Id', 'Start time', 'Completion time', 'Email', 'Name',
        'Would you like to specify a co-supervisor at this point?',
        "Co-supervisor's full name", "Co-supervisor's email address",
        'Tick which programme(s) the project is suitable for:',
        'Tick which programme(s) the project is suitable for:\n',
        'What is the maximum number of students you could take under this project title?'
    }
    
    # Start building markdown content with filtering UI
    md_content = ["<h1 style='text-align: center; font-weight: bold; margin-bottom: 20px; color: #000;'>2026 MSc Projects</h1>\n\n"]
    
    # Add instructional bullet points
    md_content.append(" <strong>Welcome to the 2026 MSc Project Selection for the Bioinformatics and AI in Biosciences programmes.</strong>\n")
    md_content.append("<ul class='instructions'>\n")
    md_content.append("  <li>Please review the following projects and identify those that align with your interests.</li>\n")
    md_content.append("  <li>Use the <b>search and filter options below</b> to find projects by keywords or programme.</li>\n")
    md_content.append("  <li>We strongly recommend contacting the project supervisor to <b>arrange a meeting</b> before applying.</li>\n")
    # Fix closing bold tag so the rest of the page is not bold
    md_content.append("  <li>Once you have reviewed all projects, please submit your choices via <b><a href='https://forms.office.com/Pages/ResponsePage.aspx?id=kfCdVhOw40CG7r2cueJYFKvg-E8GH9tMslh7hj8OGVJUNE8zSVRQQVE0S0lOMTZJSEVaUkpEMlRFQS4u' target='_blank' rel='noopener noreferrer'>this link</a></b>.</li>\n")
    md_content.append("</ul>\n\n")

    # Filter + search UI
    md_content.append("<div class='filter-container'>\n")
    md_content.append("  <h3>Browse & Filter Projects</h3>\n")
    # Mobile-only on-page search box to avoid header overlap on small screens
    md_content.append("  <div class='search-box-wrapper mobile-only'>\n")
    md_content.append("    <input id='search-box' type='text' placeholder='Search projects (e.g., python, machine learning, biology)...' oninput='searchProjects(this.value)' />\n")
    md_content.append("  </div>\n")
    md_content.append("  <div class='filter-row'>\n")
    md_content.append("    <div class='buttons'>\n")
    md_content.append("      <button class='filter-btn active' onclick='filterProjects(this, \"all\")'>All</button>\n")
    md_content.append("      <button class='filter-btn' onclick='filterProjects(this, \"ai\")'>AI in Biosciences</button>\n")
    md_content.append("      <button class='filter-btn' onclick='filterProjects(this, \"bioinf\")'>Bioinformatics</button>\n")
    md_content.append("    </div>\n")
    md_content.append("  </div>\n")
    md_content.append(f"  <p class='project-count'>Total Projects: <span id='project-count'>{len(projects)}</span></p>\n")
    md_content.append("</div>\n")
    md_content.append("<div id='projects-container'>\n")
    
    # Process each project
    for idx, project in enumerate(projects, 1):
        # Determine programme tags for filtering
        programmes = project.get('Tick which programme(s) the project is suitable for:\n', '').strip()
        has_ai = 'MSc AI in the Biosciences' in programmes if programmes else False
        has_bioinf = 'MSc Bioinformatics' in programmes if programmes else False
        
        filter_class = ""
        if has_ai and has_bioinf:
            filter_class = "project-card filter-both filter-ai filter-bioinf"
        elif has_ai:
            filter_class = "project-card filter-ai"
        elif has_bioinf:
            filter_class = "project-card filter-bioinf"
        else:
            filter_class = "project-card"
        
        md_content.append(f"\n<article class='{filter_class}' data-project-id='{idx}' data-programmes='{('ai,bioinf' if has_ai and has_bioinf else ('ai' if has_ai else ('bioinf' if has_bioinf else 'none')))}'>\n")
        title = project.get('Project title', 'Untitled').strip()
        assigned_code = project.get('Assigned_Code', f'{idx}').strip()
        md_content.append(f"<h2 class='project-title'>{assigned_code}: {title}</h2>\n")
        
        # Supervisor information
        supervisor_name = project.get('Full name', '').strip()
        supervisor_email = project.get('Email address', '').strip()
        meta_items = []
        if supervisor_name:
            if supervisor_email:
                meta_items.append(f"<li><span class='label'>Primary Supervisor</span><span class='value'>{supervisor_name} <a href='mailto:{supervisor_email}'>{supervisor_email}</a></span></li>")
            else:
                meta_items.append(f"<li><span class='label'>Primary Supervisor</span><span class='value'>{supervisor_name}</span></li>")
        
        # Co-supervisor (only if specified)
        has_cosupervisor = project.get('Would you like to specify a co-supervisor at this point?', '').strip().lower()
        if has_cosupervisor == 'yes':
            cosup_name = project.get("Co-supervisor's full name", '').strip()
            cosup_email = project.get("Co-supervisor's email address", '').strip()
            if cosup_name:
                if cosup_email:
                    meta_items.append(f"<li><span class='label'>Co-Supervisor</span><span class='value'>{cosup_name} <a href='mailto:{cosup_email}'>{cosup_email}</a></span></li>")
                else:
                    meta_items.append(f"<li><span class='label'>Co-Supervisor</span><span class='value'>{cosup_name}</span></li>")
        
        # School/Institute
        school = project.get('School/Institute', '').strip()
        if school:
            meta_items.append(f"<li><span class='label'>School/Institute</span><span class='value'>{school}</span></li>")
        
        # Research URL
        url = project.get('URL of research lab or profile page', '').strip()
        if url:
            full_url = url if url.startswith('http') else 'https://' + url
            meta_items.append(f"<li><span class='label'>Research Page</span><span class='value'><a href='{full_url}' target='_blank' rel='noopener'>{url}</a></span></li>")
        
        # Programme suitability with tick/cross (already calculated above)
        md_content.append("<div class='programme-tags'>")
        
        if has_ai:
            md_content.append("<span class='tag tag-ai'>✅ MSc AI in Biosciences</span>")
        else:
            md_content.append("<span class='tag tag-inactive'>❌ MSc AI in Biosciences</span>")
            
        if has_bioinf:
            md_content.append("<span class='tag tag-bioinf'>✅ MSc Bioinformatics</span>")
        else:
            md_content.append("<span class='tag tag-inactive'>❌ MSc Bioinformatics</span>")
        
        md_content.append("</div>\n\n")
        
        # Number of positions
        max_students = project.get('What is the maximum number of students you could take under this project title?', '').strip()
        if max_students:
            meta_items.append(f"<li><span class='label'>Positions Available</span><span class='value'>{max_students}</span></li>")
        
        # Part-time suitability
        part_time = project.get('Would this project be suitable for a part time student?', '').strip()
        if part_time:
            part_flag = 'Yes' if part_time.lower().startswith('y') else ('No' if part_time.lower().startswith('n') else part_time)
            meta_items.append(f"<li><span class='label'>Part-Time Suitable</span><span class='value'>{part_flag}</span></li>")
        
        # Project description
        description = project.get('Project description', '').strip()
        if meta_items:
            md_content.append("<ul class='project-meta'>" + ''.join(meta_items) + "</ul>")
        if description:
            paragraphs = [p.strip() for p in description.split('\n\n') if p.strip()]
            md_content.append("<div class='project-description'><h3>Project Description</h3>")
            for p in paragraphs:
                md_content.append(f"<p>{p}</p>")
            md_content.append("</div>")
        
        # Add any remaining fields not already handled
        for field, value in project.items():
            if field not in exclude_fields and value and value.strip():
                # Skip fields we've already handled
                if field in ['Full name', 'Email address', 'School/Institute', 
                           'URL of research lab or profile page', 'Project title',
                           'Project description', 'Would this project be suitable for a part time student?',
                           'Assigned_Code']:
                    continue
                
                formatted_field = field.replace('_', ' ').strip()
                if '\n' in value or len(value) > 100:
                    md_content.append(f"**{formatted_field}:**\n\n{value.strip()}\n\n")
                else:
                    md_content.append(f"**{formatted_field}:** {value.strip()}\n\n")
        
        md_content.append("</article>\n")
    
    # Close the projects container
    md_content.append("\n</div>\n\n")

    # Footer watermark credit
    md_content.append("<p class='site-watermark'><em>This website was made by Matthew Higgins (<a href='mailto:m.higgins@qmul.ac.uk'>m.higgins@qmul.ac.uk</a>).</em></p>\n\n")
    
    # Add JavaScript for filtering and search integration
    md_content.append("<script>\n")
    md_content.append("// Store current filter state\n")
    md_content.append("let currentFilter = 'all';\n")
    md_content.append("let currentSearchTerm = '';\n")
    md_content.append("\n")
    md_content.append("// Randomize project order on page load\n")
    md_content.append("function shuffleProjects(){\n")
    md_content.append("  const container = document.getElementById('projects-container');\n")
    md_content.append("  const projects = Array.from(container.querySelectorAll('.project-card'));\n")
    md_content.append("  \n")
    md_content.append("  // Fisher-Yates shuffle\n")
    md_content.append("  for(let i = projects.length - 1; i > 0; i--){\n")
    md_content.append("    const j = Math.floor(Math.random() * (i + 1));\n")
    md_content.append("    [projects[i], projects[j]] = [projects[j], projects[i]];\n")
    md_content.append("  }\n")
    md_content.append("  \n")
    md_content.append("  // Re-append in shuffled order\n")
    md_content.append("  projects.forEach(project => container.appendChild(project));\n")
    md_content.append("}\n")
    md_content.append("\n")
    md_content.append("function filterProjects(button, filter){\n")
    md_content.append("  currentFilter = filter;\n")
    md_content.append("  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));\n")
    md_content.append("  button.classList.add('active');\n")
    md_content.append("  applyFilters();\n")
    md_content.append("}\n")
    md_content.append("\n")
    md_content.append("function searchProjects(q){\n")
    md_content.append("  currentSearchTerm = q.toLowerCase();\n")
    md_content.append("  applyFilters();\n")
    md_content.append("}\n")
    md_content.append("\n")
    md_content.append("function applyFilters(){\n")
    md_content.append("  const projects = document.querySelectorAll('.project-card');\n")
    md_content.append("  let visible = 0;\n")
    # Removed auto-scroll behavior: no need to track first match
    md_content.append("  \n")
    md_content.append("  projects.forEach(p=>{\n")
    md_content.append("    const passesFilter = currentFilter === 'all' || p.classList.contains('filter-' + currentFilter);\n")
    md_content.append("    const passesSearch = !currentSearchTerm || p.textContent.toLowerCase().includes(currentSearchTerm);\n")
    md_content.append("    \n")
    md_content.append("    if(passesFilter && passesSearch){\n")
    md_content.append("      p.style.display = 'block';\n")
    md_content.append("      visible++;\n")
    md_content.append("    } else {\n")
    md_content.append("      p.style.display = 'none';\n")
    md_content.append("    }\n")
    md_content.append("  });\n")
    md_content.append("  \n")
    md_content.append("  document.getElementById('project-count').textContent = visible;\n")
    md_content.append("  \n")
    md_content.append("}\n")
    md_content.append("\n")
    md_content.append("// Integrate with MkDocs search box in header\n")
    md_content.append("document.addEventListener('DOMContentLoaded', function(){\n")
    md_content.append("  // Shuffle projects on page load\n")
    md_content.append("  shuffleProjects();\n")
    md_content.append("  \n")
    md_content.append("  // Header search (desktop)\n")
    md_content.append("  const headerSearch = document.querySelector('.md-search__input');\n")
    md_content.append("  if(headerSearch){\n")
    md_content.append("    headerSearch.placeholder = 'Search projects (e.g., python, machine learning, biology)...';\n")
    md_content.append("    headerSearch.addEventListener('input', function(e){\n")
    md_content.append("      searchProjects(e.target.value);\n")
    md_content.append("      e.stopPropagation();\n")
    md_content.append("    });\n")
    md_content.append("    headerSearch.addEventListener('focus', function(){\n")
    md_content.append("      const searchResult = document.querySelector('.md-search__output');\n")
    md_content.append("      if(searchResult) searchResult.style.display = 'none';\n")
    md_content.append("    });\n")
    md_content.append("  }\n")
    md_content.append("  // Mobile on-page search\n")
    md_content.append("  const mobileSearch = document.getElementById('search-box');\n")
    md_content.append("  if(mobileSearch){\n")
    md_content.append("    mobileSearch.addEventListener('input', function(e){\n")
    md_content.append("      searchProjects(e.target.value);\n")
    md_content.append("    });\n")
    md_content.append("  }\n")
    md_content.append("});\n")
    md_content.append("</script>\n")
    
    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(md_content)
    
    print(f"✓ Converted {len(projects)} projects from {tsv_path}")
    print(f"✓ Output written to: {output_path}")
    print(f"\n✓ Done! You can now view the projects at {output_path}")


if __name__ == "__main__":
    # Define paths
    tsv_file = Path("docs/data/Projects.tsv")
    output_file = Path("docs/index.md")
    
    # Check if TSV exists
    if not tsv_file.exists():
        print(f"Error: {tsv_file} not found!")
        exit(1)
    
    # Convert
    convert_tsv_to_markdown(tsv_file, output_file)
