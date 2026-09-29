"""
Vehicle Service App
====================

A command-line application that implements the Vehicle Service API using the
generated `vehicle_service_collection_sdk` Python SDK.

The SDK is generated from the "Vehicle Service Collection" and lives in:
    postman/sdks/Collections SDKs/Vehicle Service Collection/python

This app exposes all five API operations:
    - list      -> get_all_vehicles()
    - get       -> retrieve_a_vehicle(id)
    - create    -> create_a_vehicle(body)
    - update    -> update_a_collection(body, id)
    - delete    -> delete_a_vehicle(id)

Usage examples:
    python vehicle_app.py list
    python vehicle_app.py get 1
    python vehicle_app.py create --nick-name "The Lisa Marie" --vin 4M2DV11W4RDJ53329 \
        --make Mercury --model Villager --year 1994 --miles 159864
    python vehicle_app.py update 1 --miles 159999
    python vehicle_app.py delete 1

Configuration is read from environment variables (see .env.example):
    VEHICLE_API_BASE_URL   Base URL of the Vehicle Service API (or mock server)
    VEHICLE_API_KEY        API key for authentication (optional for local mock)
"""

import argparse
import json
import os
import sys

from vehicle_service_collection_sdk import VehicleServiceCollectionSdk
from vehicle_service_collection_sdk.models import CreateAVehicleRequest


def build_sdk() -> VehicleServiceCollectionSdk:
    """Create and configure the SDK client from environment variables."""
    base_url = os.getenv("VEHICLE_API_BASE_URL", "http://localhost:4500")
    api_key = os.getenv("VEHICLE_API_KEY", "")

    kwargs = {"base_url": base_url, "timeout": 10}
    if api_key:
        kwargs["api_key"] = api_key

    return VehicleServiceCollectionSdk(**kwargs)


def _print_result(result) -> None:
    """Pretty-print an SDK result whether it is a dict, model, or string."""
    if result is None or result == "":
        print("(no content)")
        return
    try:
        # pydantic models expose model_dump(); dicts/lists serialize directly
        if hasattr(result, "model_dump"):
            result = result.model_dump()
        print(json.dumps(result, indent=2, default=str))
    except (TypeError, ValueError):
        print(result)


# --- Command handlers --------------------------------------------------------

def cmd_list(sdk, _args) -> None:
    """List all vehicles."""
    _print_result(sdk.vehicle_service_collection_sdk.get_all_vehicles())


def cmd_get(sdk, args) -> None:
    """Retrieve a single vehicle by id."""
    _print_result(sdk.vehicle_service_collection_sdk.retrieve_a_vehicle(args.id))


def cmd_create(sdk, args) -> None:
    """Create a new vehicle."""
    body = CreateAVehicleRequest(
        nick_name=args.nick_name,
        vin=args.vin,
        make=args.make,
        model=args.model,
        year=args.year,
        miles=args.miles,
    )
    _print_result(
        sdk.vehicle_service_collection_sdk.create_a_vehicle(request_body=body)
    )


def cmd_update(sdk, args) -> None:
    """Update an existing vehicle by id."""
    body = CreateAVehicleRequest(
        nick_name=args.nick_name,
        vin=args.vin,
        make=args.make,
        model=args.model,
        year=args.year,
        miles=args.miles,
    )
    _print_result(
        sdk.vehicle_service_collection_sdk.update_a_collection(
            request_body=body, id_=args.id
        )
    )


def cmd_delete(sdk, args) -> None:
    """Delete a vehicle by id."""
    sdk.vehicle_service_collection_sdk.delete_a_vehicle(args.id)
    print(f"Deleted vehicle {args.id}")


# --- Argument parsing --------------------------------------------------------

def _add_vehicle_fields(parser: argparse.ArgumentParser) -> None:
    """Attach the shared vehicle body fields to create/update subparsers."""
    parser.add_argument("--nick-name", dest="nick_name", help="Vehicle nickname")
    parser.add_argument("--vin", help="Vehicle identification number")
    parser.add_argument("--make", help="Manufacturer, e.g. Mercury")
    parser.add_argument("--model", help="Model, e.g. Villager")
    parser.add_argument("--year", help="Model year, e.g. 1994")
    parser.add_argument("--miles", type=int, help="Odometer reading")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Vehicle Service API client (backed by the generated SDK)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all vehicles").set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Retrieve a vehicle by id")
    p_get.add_argument("id", help="Vehicle id")
    p_get.set_defaults(func=cmd_get)

    p_create = sub.add_parser("create", help="Create a new vehicle")
    _add_vehicle_fields(p_create)
    p_create.set_defaults(func=cmd_create)

    p_update = sub.add_parser("update", help="Update a vehicle by id")
    p_update.add_argument("id", help="Vehicle id")
    _add_vehicle_fields(p_update)
    p_update.set_defaults(func=cmd_update)

    p_delete = sub.add_parser("delete", help="Delete a vehicle by id")
    p_delete.add_argument("id", help="Vehicle id")
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    sdk = build_sdk()
    try:
        args.func(sdk, args)
    except Exception as exc:  # noqa: BLE001 - surface any SDK/request error to the CLI
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
