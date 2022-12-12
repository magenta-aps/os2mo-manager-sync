<!--
SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->

## SD MANAGER SYNC

***
This repository contains the OS2MO manager script for updating managers. <br>Managers are updated based on data imported from SD-Løn prior to running this integration. <br>

It has two main goals: <br>

1. **Terminate managers with no active engagement in the org-unit they're allocated as manager. <br>**
2. **Allocate new managers based on info in special child org-units with name ending in *"_leder"*. <br>**



***
## Usage
***

If needed set enviromental variabels in `docker-compose.yaml` (More info on those further down)

To start the container using `docker-compose`: <br>

	docker-compose up -d

After the container is up and running, the script can be run manually by triggering an `FastAPI` endpoint. <br>

 * By using the GUI at:<br>
```http://localhost:8000/docs```
and triggering `/trigger/all`.

 * Calling the endpoint from terminal: <br>
```$ curl -X 'POST' 'http://localhost:8000/trigger/all'``` <br>

As it checks and updates managers you will get a lot of output in `docker logs`, especially if you have opted for `debug`information from logs.

Once the script has finished the last lines will look like this:

```
sd_managerscript_1  | 2022-12-09 10:38.30 [info     ] Filter Managers
sd_managerscript_1  | 2022-12-09 10:38.30 [info     ] Updating Managers
sd_managerscript_1  | 2022-12-09 10:38.30 [info     ] Updating managers complete!

```
***
## Cycle rundown
### This decribes the steps taken when script is triggered.


 * <span style="color:blue">**All current manager roles are checked to verify the employee has an active engagement in the organisation unit they are placed.**</span>
    * **If not: manager role get terminated (manager roles end date set to today)**  <br><br>

 * <span style="color:blue">**For every organisation unit (org-unit) with `name` ending in `_leder` and name NOT prepended with `Ø_`**</span>
 <br><p align="center">
     ![_leder org-unit](readme_images/_leder.png  "_leder org-unit") </p>
    * <span style="color:blue">**Get all employees with association to `_leder` unit.**  <br>
<p align="center">

   ![Tilknytninger](readme_images/tilknytning.png  "Tilknytninger")</p>
    <br>
    * <span style="color:blue">**Check each employee has an active engagement in parent org-unit.**</span>
    <br>
    * <span style="color:blue">**If more than one employee with association in `_leder` org-unit, check which employee has the latest `engagement from` date. The one with latest engagement date becomes manager in parent org-unit.**</span> <br>
    <br>
    * <span style="color:blue">**The manger roles `manager level` is based on the org-unit level, in which the manager role is assigned at:**</span><br><br><p align="center">
    ![Manager level](readme_images/manager_level.png  "Manager level")
    <br></p>
    * <span style="color:blue">**If parent org-unit has `_led-adm` in name the manager will also become leder of this org-units parent org-unit.**</span><br>
    (Notice: Manager level is based on org-unit level from higeste ranking org-unit)
    <br><p align="center">
    ![led-adm](readme_images/_led-adm.png  "led-adm")
    </p>
    *In the above illustration, manager fetched from `_leder` unit becomes manager in not only "Byudvikling" but also "Borgmesterens Afdeling" as "Byudvikling is marked as an `led-adm` unit.
  Manager level is then based on org-unit level from "Borgmesterens Afdeling"*
  <br>
 * <span style="color:blue">**Once a manager has been selected based on above criterias, associations for all other employees in `_leder` unit are terminated.  <br>Leaving just one association in `_leder` unit.**</span>

***
## Enviromental Variables
***
`MO_URL`:  Base URL for `OS2MO`
<br>
`CLIENT_ID`:  Login for this integration (dipex) client
<br>
`CLIENT SECRET`: Password for access to `OS2MO`
<br>
`ROOT_UUID`: UUID of the root organisation unit. Instance dependant.
<br>
`MANAGER_TYPE_UUID`: Default UUID for `Manager type`. Instance dependant.
<br>
`RESPONSIBILITY_UUID`: Default UUID for `Manager type`. Instance dependant.
<br>
`MANAGER_LEVEL_MAPPING`: Dict with `org-unit level UUID` classes as keys and `manager level UUID` as values. Used to map from `org_unit_level` to `manager_level`.


***
## Development
***
### Prerequisites

- [Poetry](https://github.com/python-poetry/poetry)

### Getting Started

1. Clone the repository:
```
git clone git@git.magenta.dk:rammearkitektur/os2mo-manager-sync.git
```

2. Install all dependencies:
```
poetry install
```

3. Set up pre-commit:
```
poetry run pre-commit install
```

### Running the tests

You use `poetry` and `pytest` to run the tests:

`poetry run pytest`

You can also run specific files

`poetry run pytest tests/<test_folder>/<test_file.py>`

and even use filtering with `-k`

`poetry run pytest -k "Manager"`

You can use the flags `-vx` where `v` prints the test & `x` makes the test stop if any tests fails (Verbose, X-fail)

### Injecting test data into OS2MO
Test data have been prepared for local development. To use the test data nd inject it, it requires a running `OS2MO` instance locally, as well as the standard test data from Kolding, which is included in `OS2MO` repository.

Before using this integration locally you need to clone and run the `OS2MO` container from [OS2MO repo](https://git.magenta.dk/rammearkitektur/os2mo):<br>
Once cloned you can start main `OS2MO` container using:
```docker-compose up --build -d```

You can now inject test data from this repository by changing folder to where this repository is located locally.
Then run the folling command:

```
poetry run python tests/test_data/inject_test_data.py "603f1c82-d012-4d04-9382-dbe659c533fb"
```
UUID passed as an parameter is required password

### Development info

Sending and fetching data to/from `OS2MO` is done using a `GraphQL` client imported from `Ra-clients` [repos here](https://git.magenta.dk/rammearkitektur/ra-clients)

***

## Authors

Magenta ApS <https://magenta.dk>
***
## License

This project uses: [MPL-2.0](MPL-2.0.txt)

This project uses [REUSE](https://reuse.software) for licensing.
All licenses can be found in the [LICENSES folder](LICENSES/) of the project.
