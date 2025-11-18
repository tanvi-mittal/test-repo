## :warning: Please read these instructions carefully and entirely first
* Clone this repository to your local machine.
* Use your IDE of choice to complete the assignment.
* When you have completed the assignment, you need to  push your code to this repository and [mark the assignment as completed by clicking here](https://app.snapcode.review/submission_links/5e88da96-56a4-44ee-acc9-0141381b3312).
* Once you mark it as completed, your access to this repository will be revoked. Please make sure that you have completed the assignment and pushed all code from your local machine to this repository before you click the link.

## Operability Take-Home Exercise

Welcome to the start of our recruitment process for Operability Engineers. It was great to speak to you regarding an opportunity to join the Equal Experts network!

Please write code to deliver a solution to the problems outlined below.

We appreciate that your time is valuable and do not expect this exercise to **take more than 90 minutes**. If you think this exercise will take longer than that, I **strongly** encourage you to please get in touch to ask any clarifying questions.

### Submission guidelines
**Do**
- Provide a README file in text or markdown format that documents a concise way to set up and run the provided solution.
- Take the time to read any applicable API or service docs, it may save you significant effort.
- Make your solution simple and clear. We aren't looking for overly complex ways to solve the problem since in our experience, simple and clear solutions to problems are generally the most maintainable and extensible solutions.

**Don't**

Expect the reviewer to dedicate a machine to review the test by:

- Installing software globally that may conflict with system software
- Requiring changes to system-wide configurations
- Providing overly complex solutions that need to spin up a ton of unneeded supporting dependencies. We aspire to keep our dev experiences as simple as possible (but no simpler)!
- Include identifying information in your submission. We are endeavouring to make our review process anonymous to reduce bias.

### Exercise
If you have any questions on the below exercise, please do get in touch and we’ll answer as soon as possible.

#### Build an API, test it, and package it into a container
- Build a simple HTTP web server API in any general-purpose programming language[^1] that interacts with the GitHub API and responds to requests on `/<USER>` with a list of the user’s publicly available Gists[^2].
- Create an automated test to validate that your web server API works. An example user to use as test data is `octocat`.
- Package the web server API into a docker container that listens for requests on port `8080`. You do not need to publish the resulting container image in any container registry, but we are expecting the Dockerfile in the submission.
- The solution may optionally provide other functionality (e.g. pagination, caching) but the above **must** be implemented.

Best of luck,
Equal Experts
__________________________________________
[^1]: For example Go, Python or Ruby but not Bash or Powershell.
[^2]: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28


## Instructions to run the API

### Run Locally
Follow these steps to run the project on your local machine:

#### 1. Clone the repository from github
```bash
git clone https://github.com/EqualExperts-Assignments/equal-experts-fierce-ambitious-alert-animal-a6a2d020bb69.git
cd equal-experts-fierce-ambitious-alert-animal-a6a2d020bb69
```

#### 2.(Optional) Create and activate a virtual environment
```bash
# Use either of the following depending on your system
python -m venv venv
# or
python3 -m venv venv

# Activate the environment
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

#### 3. Install dependencies
```bash
# Use either of the following depending on your system
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

#### 4. Run the Flask app
```bash
python app.py
```
Visit the API at: http://localhost:8080/octocat

You can replace octocat with any GitHub username:
```bash
http://localhost:8080/<username>
```

### Run using Docker

#### 1.Build the docker image
```bash
docker build -t github-gist-api .
```
#### 2. Run the container
```bash
docker run -p 8080:8080 github-gist-api
```
#### 3. Test the API
```bash
curl http://localhost:8080/octocat
```

Or open in your browser:
```bash
http://localhost:8080/octocat
http://localhost:8080/<username>
```

#### Run Tests
```bash
pytest test_cases.py
```

### Project Structure
```bash
equal-experts-fierce-ambitious-alert-animal-a6a2d020bb69/
├── app.py              # Flask app
├── test_app.py       # Pytest test suite
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker container setup
└── README.md           # Project documentation
```
