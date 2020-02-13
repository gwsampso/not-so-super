# Not So Super
## Which funds are not so super?
The challenge to compare fund performance is most acute for choice super products. Astoundingly, super funds aren’t required to provide simple, comparable information on the fees and returns of choice products

This tool should be used by anyone who wants to check on their fund, with the appropriate focus on long-term performance.You can compare performance at the click of a mouse button.

You can adjust the products in the "Filters" tab, and the ordering/ranking on the tables

So which funds really are super?

The data in these tabs is drawn from the latest published information provided bysuper funds to the Australian Prudential Regulation Authority (APRA).

## Development
```{sh}
git clone https://github.com/gwsampso/not-so-super.git
cd not-so-super
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```
and run,

```{sh}
python index.py
```
The application should be up and running at http://localhost:8050/not-so-super/not-so-super

## Screenshots