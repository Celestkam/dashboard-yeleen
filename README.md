This project was developed as part of my MBA in Project Management at CESAG Dakar. It focuses on the design and implementation of a data-driven dashboard (Yeleen) to support monitoring, evaluation, accountability, and learning (MEAL) for energy and development projects in Burkina Faso.

The dashboard integrates ODK-collected data with a relational database and interactive visualization, providing decision-makers with real-time insights into project performance.

Objectives

Collect and clean field data via ODK surveys.

Store project indicators in a relational database (indicateurs.db).

Develop an interactive dashboard (dashboard.py) to monitor:

Access to electricity and renewable energy penetration

Project progress and efficiency metrics

Community-level indicators collected in the field

Support project teams and stakeholders with evidence-based decision-making.

Tools & Technologies

ODK (Open Data Kit) → Field data collection (households, communities, projects).

Python → Data cleaning, processing, dashboard scripts.

Database → SQLite (indicateurs.db) for storing indicators.

Visualization → Streamlit for interactive charts and KPIs.

Environment → Jupyter, Google Colab, GitHub.

Repository Structure

create_db.py → Script to build and populate the SQLite database with ODK data.

dashboard.py → Streamlit app for visualization.

indicateurs.db → SQLite database containing ODK-collected indicators.

requirements.txt → Python dependencies.

logos/ → Visual assets for dashboard branding.
