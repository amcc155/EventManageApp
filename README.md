# 📋 i211 Flask Template

- 📔 This is *your* repository, make it your own!
- ✏️ The `README.md` is a place to take notes about your work and workflow
- 📃 Read below, we've included some notes to get your started

## ⚡ Quickstart

### MacOS / WSL / Linux / ChromeOS

Clone the repository (replacing `REPO_NAME`):

```bash
git clone https://github.iu.edu/i211fa2023/REPO_NAME.git
cd REPO_NAME
```

Create a `venv` environment, activate it, and install dependencies with `pip`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Check that `flask` runs without errors:

```bash
python -m flask --version
```

<details>
<summary><strong>Debugging</strong>: Did <code>flask</code> fail with an error: <code>ImportError: cannot import name 'Mapping' from 'collections'</code>?</summary>

> Run the patch script:
>
> ```powershell
> python patch_jinja.py
> ```

</details>

### PowerShell + Windows (Not Recommended)

<details>
<summary>Why is this Not Recommended?</summary>

> Our goal is to build web applications that run in a Unix-like environment. Accomplishing this goal is easiest when we can *develop* and *deploy* to Unix-like environments.
>
> Microsoft Windows has a different set of *development tools* (shells, compilers, and debuggers) and an architecture which, for historical reasons, is quite different from the Unix-like operating systems that >98% of the Internet run on.
>
> Covering "how to develop for the Windows platform" is therefore mostly a topic for another time. We only recommend this if:
>
> - You already have experience with the Windows development ecosystem
> - You are comfortable with Unix environments from previous experience, and are comfortable translating between Windows and Unix
> - You have an older Windows environment that is incompatible with WSL

</details>

<details>
<summary>Create a venv environment, activate it, and install requirements.</summary>

> ```powershell
> python -m venv venv
> .\venv\Scripts\Activate.ps1
> pip install -r requirements.txt
> ```

</details>

<details>
<summary><strong>Debugging</strong>: Do you see a red permissions error when activating the environment?</summary>

> You might need to set the execution policy on your machine. This should only need to be done once:
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

</details>

## 🏃 Starting a Development Server

The default package name is `flaskapp`. Running the package as a module `-m` starts the server on http://localhost:5000

```bash
python -m flaskapp
```

Alternatively, starting with "*Run and Debug*" in Visual Studio Code (<kbd>F5</kbd>) will also start the server in debug mode.

<details>
<summary><strong>Debugging</strong>: Does VS Code tell you "No module named flask"?</summary>

> Assuming you already installed dependencies with:
>
> ```bash
> source venv/bin/activate
> pip install -r requirements.txt
> ```
>
> It's possible that Visual Studio Code is not locating the `venv` environment. You can set the Python interpreter in VS Code by opening the command palette (<kbd>^ Ctrl</kbd> + <kbd>⇧ Shift</kbd> + <kbd>P</kbd>, or: <kbd>⌘ Cmd</kbd> + <kbd>⇧ Shift</kbd> + <kbd>P</kbd>) and typing `Python: Select Interpreter`. Then select the `venv` environment.
>
> The slightly more manual approach is to open the VS Code terminal, activate the `venv` environment, and start `flaskapp`:
>
> ```bash
> source venv/bin/activate
> python -m flaskapp
> ```
>
> This might mean we need to recreate the `venv` environment. If the Python extension is not finding an interpreter, it can be a sign that there is a compatibility issue with the environment (see also: https://code.visualstudio.com/docs/python/environments#_working-with-python-interpreters).

</details>


## 🚀 Deploying

### First-time Deploy

`ssh` into silo, replacing `USERNAME` with your IU username:

```bash
ssh USERNAME@silo.luddy.indiana.edu
```

Clone the project/lecture repositories, replacing `USERNAME` with your IU username.

```bash
git clone https://github.iu.edu/i211fa2023/USERNAME_i211_lecture.git ~/cgi-pub/i211_lecture
```

```bash
git clone https://github.iu.edu/i211fa2023/USERNAME_i211_project.git ~/cgi-pub/i211_project
```

### Subsequent Deploys

After `git` repositories are set up, you can deploy changes using `ssh`:

```bash
ssh USERNAME@silo.luddy.indiana.edu
cd ~/cgi-pub/i211_lecture
git restore .
git pull
```

```bash
ssh USERNAME@silo.luddy.indiana.edu
cd ~/cgi-pub/i211_project
git restore .
git pull'
```

## 🧑‍💻 Checking your work

Once deployed, your changes should immediately be visible:

- https://cgi.luddy.indiana.edu/~USERNAME/i211_lecture/
- https://cgi.luddy.indiana.edu/~USERNAME/i211_project/

## 🐛 Debugging

Try and avoid *debugging in production*, but if you must:

- [CGI Production Debugger](https://cgi.luddy.indiana.edu/~hayesall/cgi-production-debugger/)

---

## 📝 Further Reading

### Primary Sources

|  | url | summary |
| :--- | :---- | :----- |
| Bootstrap 5.3 | [Bootstrap 5.3 Intro](https://getbootstrap.com/docs/5.3/getting-started/introduction/) | "Bootstrap is a powerful, feature-packed frontend toolkit." |
| Jinja 2.10.x | [Jinja 2.10 Docs](https://jinja.palletsprojects.com/en/2.10.x/) | Jinja is a templating language for Python. |
| Flask 1.1.x | [Flask 1.1.x Docs](https://flask.palletsprojects.com/en/1.1.x/) | Flask is a web app microframework |
| `templates/base.html` | [Bootstrap Sticky Footer Navbar](https://getbootstrap.com/docs/5.3/examples/sticky-footer-navbar/) | The `base.html` here is based off the Bootstrap 5.3 "*Sticky footer with fixed navbar*" template. |
| Luddy CGI Server | [CGI Server - Luddy Policies](https://policies.luddy.indiana.edu/it/guides/web/run-cgi-scripts-on-web-server.html) | The Luddy cgi server allows the running of arbitrary programs (e.g. perl, python, scheme, bash, etc). |

### Common Operations

Logging into `silo`:

```bash
ssh USERNAME@silo.luddy.indiana.edu
```

Debugging cgi errors:

```bash
ssh USERNAME@silo.luddy.indiana.edu
ssh USERNAME@cgi.luddy.indiana.edu
less +F /var/log/apache2/error.log
```

Logging into MariaDB (replace USER/PASSWORD/DATABASE):

```bash
mysql -h db.luddy.indiana.edu -u USER --password=PASSWORD -D DATABASE
```

### Other Notes

**Q**: *How do I know what packages are installed on the server?*

**A**: Here's a one-liner:

```bash
pip freeze | grep "click\|Flask\|itsdangerous\|Jinja2\|MarkupSafe\|Werkzeug\|PyMySQL"
```
