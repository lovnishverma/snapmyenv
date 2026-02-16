---
title: 'snapmyenv: A Lightweight Solution for Embedded Reproducibility in Jupyter Notebooks'
tags:
  - Python
  - reproducibility
  - Jupyter
  - Google Colab
  - dependency management
  - education
authors:
  - name: Lovnish Verma
    orcid: 0009-0009-3992-030X
    affiliation: 1
affiliations:
 - name: National Institute of Electronics and Information Technology (NIELIT), Ropar, India
   index: 1
date: 16 February 2026
bibliography: paper.bib
---

# Summary

`snapmyenv` is a Python library designed to enhance computational reproducibility in data science workflows, specifically for users of Jupyter Notebooks and Google Colab. Unlike traditional environment managers that rely on external configuration files, `snapmyenv` captures the comprehensive runtime state—including Python version, operating system details, and exact package versions—and embeds this information directly into the notebook's JSON metadata. By binding the environment definition to the code artifact itself, `snapmyenv` ensures that the execution context travels with the notebook, allowing collaborators to restore the precise runtime environment with a single command.

# Statement of Need

The "reproducibility crisis" in computational science is exacerbated by the complexity of managing software environments [@Baker:2016]. While Jupyter Notebooks have become the *de facto* standard for sharing data science work [@Kluyver:2016], they often fail to execute on different machines due to missing or mismatched dependencies. This issue is particularly acute in two contexts:

1.  **Ephemeral Cloud Environments**: In platforms like Google Colab [@Bisong:2019], the runtime is reset after every session. Researchers often share `.ipynb` files without accompanying environment descriptors, rendering the code non-executable for collaborators.
2.  **Education**: In classroom settings, students often struggle with complex environment management tools like Docker. When submitting assignments, they may unknowingly rely on local packages that the instructor does not have installed, leading to the "it works on my machine" friction during grading.

`snapmyenv` bridges this gap by treating the notebook file as a self-contained unit of reproducibility. It targets researchers, educators, and students who need a zero-friction method to preserve their computational context without the cognitive overhead of containerization.

# Design and Implementation

`snapmyenv` was engineered with a "zero-dependency" philosophy to ensure that the tool itself does not introduce version conflicts. It relies exclusively on the Python standard library (`sys`, `json`, `subprocess`, `platform`) for all core operations.

The library operates through three primary modules:

1.  **Capture and Validation**: The `capture` module queries the current environment state. Unlike simple requirements generators, `snapmyenv` employs strict data models (defined in `models.py`) to validate package names and versions before serialization. It also captures platform architecture (e.g., `x86_64` vs `arm64`) to warn users of potential binary incompatibilities during restoration.
2.  **Metadata Embedding**: The `notebook` module parses the `.ipynb` JSON structure and injects the snapshot under a dedicated `snapmyenv_snapshot` metadata key. This approach ensures compatibility with standard Jupyter tools while keeping the environment data persistent.
3.  **Restoration and Safety**: The `restore` module provides a safety-first approach to environment recreation. It includes a `dry_run` capability, allowing users to preview changes before installation. Furthermore, it detects if the code is running in Google Colab and adjusts installation strategies accordingly, handling the unique permission structures of cloud runtimes.

# State of the Field

Environment management in Python is a mature field, yet existing tools often present a high barrier to entry for novice users or disconnect the code from its environment:

* **`pip freeze > requirements.txt`**: This standard practice generates a separate file that is easily lost, renamed, or desynchronized from the notebook it supports. It also lacks metadata about the Python version or operating system.
* **Docker**: While Docker provides robust reproducibility [@Boettiger:2015], it adds significant complexity and resource overhead. For exploratory analysis or educational contexts, requiring students to write `Dockerfiles` is often prohibitive.
* **Binder**: Binder is excellent for hosting executable environments [@ProjectJupyter:2018], but it relies on repository configuration files that must exist *before* the environment is built. `snapmyenv`, conversely, captures the *current* interactive state "as-is."
* **`pipreqs` / `pigar`**: These tools statically analyze code to generate requirements. While useful, they can miss dynamically imported packages or non-obvious dependencies. `snapmyenv` takes a snapshot of the *actual* installed environment, ensuring that what ran on the author's machine is exactly what is recorded.

`snapmyenv` differentiates itself by prioritizing **portability** (single-file distribution) and **simplicity** (no external config files), making it uniquely potential for the long tail of scientific scripts and classroom assignments.

# Acknowledgements

This project was developed with guidance and support from Dr. Sarwan Singh, Joint Director at NIELIT Ropar.

# References
