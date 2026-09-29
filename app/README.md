# Vehicle Service App

A command-line Python application that implements the **Vehicle Service API**
using the generated `vehicle_service_collection_sdk` Python SDK.

The SDK is generated from the **Vehicle Service Collection** and lives at:

```
postman/sdks/Collections SDKs/Vehicle Service Collection/python
```

This app wraps all five API operations exposed by that SDK.

## Operations

| Command  | SDK method                          | HTTP                    |
| -------- | ----------------------------------- | ----------------------- |
| `list`   | `get_all_vehicles()`                | `GET /vehicles`         |
| `get`    | `retrieve_a_vehicle(id)`            | `GET /vehicles/:id`     |
| `create` | `create_a_vehicle(body)`            | `POST /vehicles`        |
| `update` | `update_a_collection(body, id)`     | `PATCH /vehicles/:id`   |
| `delete` | `delete_a_vehicle(id)`              | `DELETE /vehicles/:id`  |

## Setup

Requires **Python >= 3.9** (the SDK's minimum supported version).

```bash
cd app

# (recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate

# install the app's dependency (the generated SDK, in editable mode)
pip install -r requirements.txt
```

## Configuration

The app reads two environment variables:

| Variable               | Description                                   | Default                  |
| ---------------------- | --------------------------------------------- | ------------------------ |
| `VEHICLE_API_BASE_URL` | Base URL of the Vehicle Service API / mock    | `http://localhost:4500`  |
| `VEHICLE_API_KEY`      | API key for authentication (optional locally) | *(empty)*                |

Copy `.env.example` to `.env` and adjust, or export the variables directly:

```bash
export VEHICLE_API_BASE_URL="http://localhost:4500"
export VEHICLE_API_KEY=""
```

> **Tip:** You can point `VEHICLE_API_BASE_URL` at the Postman **Vehicle Service Mock**
> server (its `http://localhost:<port>` URL) to run the app fully offline.

## Usage

```bash
# List all vehicles
python vehicle_app.py list

# Retrieve a single vehicle
python vehicle_app.py get 1

# Create a vehicle
python vehicle_app.py create \
    --nick-name "The Lisa Marie" \
    --vin 4M2DV11W4RDJ53329 \
    --make Mercury \
    --model Villager \
    --year 1994 \
    --miles 159864

# Update a vehicle (only pass the fields you want to change)
python vehicle_app.py update 1 --miles 159999

# Delete a vehicle
python vehicle_app.py delete 1
```

## Project structure

```
app/
├── vehicle_app.py     # CLI app implementing the API via the SDK
├── requirements.txt   # installs the generated SDK (editable)
├── .env.example       # sample configuration
└── README.md          # this file
```
