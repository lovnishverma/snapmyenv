---
title: 'snapmyenv: A Lightweight Solution for Embedded Reproducibility in Jupyter Notebooks'
tags:
  - Python
  - reproducibility
  - Jupyter
  - Google Colab
  - dependency management
  - data science
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

`snapmyenv` is a Python library designed to enhance computational reproducibility in data science workflows, specifically for users of Jupyter Notebooks and Google Colab. It captures the comprehensive runtime environment—including Python version, operating system details, and exact package versions—and embeds this information directly into the notebook's metadata. By binding the environment definition to the code artifact itself, `snapmyenv` eliminates the friction of managing external dependency files (like `requirements.txt`) and allows researchers to restore the precise execution environment with a single command.

# Statement of Need

The "reproducibility crisis" in computational science is exacerbated by the complexity of managing software environments [@Baker:2016]. While Jupyter Notebooks have become the *de facto* standard for sharing data science work [@Kluyver:2016], they often fail to execute on different machines due to missing or mismatched dependencies—the classic "it works on my machine" problem.

This issue is particularly acute in ephemeral cloud environments like Google Colab [@Bisong:2019], where the runtime is reset after every session. Researchers frequently share `.ipynb` files without accompanying environment descriptors, rendering the code non-executable for collaborators or peer reviewers.

Existing solutions often have a high barrier to entry or disconnect the code from its environment:

* **`pip freeze > requirements.txt`**: Generates a separate file that is easily lost, renamed, or desynchronized from the notebook it supports.
* **Docker**: Provides robust reproducibility [@Boettiger:2015] but adds significant complexity and overhead, which can be prohibitive for exploratory analysis or users without systems engineering expertise.
* **Binder**: Excellent for hosting, but relies on repository configuration files that must exist *before* the environment is built, rather than capturing an interactive session's state "as-is" [@ProjectJupyter:2018].

`snapmyenv` bridges this gap by treating the notebook file as a self-contained unit of reproducibility. It targets researchers and data scientists who need a zero-friction method to preserve their computational context. By leveraging the standard library for all core operations, `snapmyenv` ensures that the tool itself does not introduce dependency conflicts, providing a lightweight yet robust mechanism for environment preservation.

# State of the Field

Environment management in Python is a crowded field, with tools like `Conda`, `Poetry`, and `Virtualenv` serving as primary package managers. However, these tools focus on *creating* environments, not necessarily *snapshotting and embedding* them into portable artifacts.

`snapmyenv` differentiates itself through its storage mechanism. While standard practices dictate storing dependencies in `requirements.txt` (pip), `environment.yml` (conda), or `pyproject.toml` (poetry), `snapmyenv` writes directly to the `.ipynb` JSON metadata structure. This ensures that wherever the notebook goes—email, Slack, or a Learning Management System (LMS)—its environment definition travels with it.

Key features include:
1.  **Platform Awareness**: Captures OS and architecture details to warn users of potential binary incompatibilities.
2.  **Colab Integration**: specifically detects and handles the Google Colab runtime, which is a primary use case for students and educators in the developing world.
3.  **Safety Mechanisms**: Includes "dry-run" capabilities to preview environment changes before installation, preventing accidental overwrites of local configurations.

# Acknowledgements

This project was developed with guidance and support from Dr. Sarwan Singh, Joint Director at NIELIT Ropar. I also acknowledge the open-source community for the robust tooling that makes projects like this possible.

# References
