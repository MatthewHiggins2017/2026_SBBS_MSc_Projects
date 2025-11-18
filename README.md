# 2025 QMUL Project Allocation MSc 

## Creating the Index Page From Project TSV 

The docs/index.md page is auto-generated from the tab-separated file at docs/data/Projects.tsv. No personal or project content is exposed in this README; only the column headers used for generation are shown.

Columns present in docs/data/Projects.tsv (headers only):
- Id
- Start time
- Completion time
- Email
- Name
- Full name
- Email address
- School/Institute
- URL of research lab or profile page
- Would you like to specify a co-supervisor at this point?
- Co-supervisor's full name
- Co-supervisor's email address
- Project title
- Tick which programme(s) the project is suitable for:
- What is the maximum number of students you could take under this project title?
- Project description
- Would this project be suitable for a part time student?

Rough generation process:
- Read docs/data/Projects.tsv (UTF-8, tab-delimited), treating the first row as headers.
- Clean/normalise headers (trim whitespace, collapse line breaks in headers).
- For each row, map fields by header and construct a Markdown section (e.g., title, supervisors, school, suitability, description).
- Optionally group or filter by programme and/or school.
- Write the composed content to docs/index.md before mkdocs build/serve.

### Setting up

It is best to do this in a fresh conda environment which you can make with

```
mamba create -n mkdocs -c conda-forge mkdocs-material -y
```

Then on your computer clone the repository:

```
git clone https://github.com/xxx
```

Checkout the `dev` branch:

```
git checkout dev
```

Activate the conda environment

```
conda activate mkdocs-material
```

Then go into the folder and run mkdocs serve

```
mkdocs serve
```

### Adding new tutorials

If you need add a new tutorial just create a new markdown file in `docs/<subdirectory>`. If you are running mkdocs serve your changes will automatically force the browser to refresh.

Adding the tutorial to the menu is done in `mkdocs.yml` under the `nav` section. Which has the folliwing format:

```yaml
nav:
  - Home: 
    - index.md
    - connecting-github.md
  - Introduction: 
      - introduction/intro-to-linux.md
      - introduction/mapping.md
      - introduction/variant-detection.md
      - introduction/assembly.md
      - introduction/task.md
```

To add a new tutorial you can just add a new line under the relevant section. The indentation is important so make sure you keep it the same.

#### Images

All images can be placed using the following notation

```
![mapping_1](../img/Mapping_1.jpg)
```

#### Questions

If there is a question that you want the participant to think about you can format it like this:

```
!!! question "Question 1"
    Is this a question?
```

If your question has a specific answer you can use the following formatting

```
!!! question
    === "Question 1"
        Is this a question?
    === "Answer 1"
        This is an answer
```

#### Information

Tips and information can be inserted using the following:

```
!!! info
    This is some information
```

#### Terminal output

If you want to put in some expected output from the terminal that the participants can compare to then this will work:

```
!!! terminal "Terminal output"
    ```
    This is osme terminal output
    ```
```
#### Code

Code can be inserted with the the triple backticks (without the backslash):

```
\```
some_command -a parameter1
\```
```


