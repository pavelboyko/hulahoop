# What is Hulahoop

Hulahoop is a service that helps teams collect, analyze and fix mistakes in ML-based products. Hulahoop aims to make ML quality assurance more productive through repeatable transparent processes and automation.

**⚠️ Hulahoop is currently in early development and features and APIs are likely to change quite often.**

## Purpose

Successful software products based on machine learning have amazing features but frequently require constant maintenance and babysitting of the ML models used.
The purpose of Hulahoop is to make the process of identifying and eliminating ML mistakes repeatable and transparent.
Hulahoop helps teams to automate the collection of ML mistakes examples, the systematization of similar examples for various issues, the analysis and resolution of issues, and regression control.
Hulahoop gives product stakeholders a transparent picture of what mistakes ML makes, and how and when they are fixed.

Signs that you may benefit from Hulahoop:

- you develop or operate a software product based on machine learning
- your ML models work with unstructured data like images, video, audio, text
- your clients are sensitive to ML mistakes one way or another
- you are committed to service level agreements on the accuracy of your ML
- you have an ML QA team that is responsible for detecting and fixing bugs in ML

## Beliefs

We believe that quality assurance in machine learning is a complex creative work that goes far beyond the "label more data" mantra and that the path to quality lies through a deep understanding of the nuances of a particular product, data and model stack. Therefore, we are developing Hulahoop as open-source software with an emphasis on extensibility and customization.

We also believe that every company should be able to fully own their data, which is why we are developing Hulahoop with the ability to self-host, although, a managed Hualahoop service may someday appear.

## Docs

- How to collect examples with the [capture endpoint](docs/capture.md).
- [Client-side example grouping](docs/fingerprint.md) with the fingerprint field.

## Developing locally & Contributing

- [Starting developing locally](docs/dev_start.md)
