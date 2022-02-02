from fhirpy import SyncFHIRClient
import pytz
import datetime

# Create an instance
client = SyncFHIRClient(
    'http://hapi.fhir.org/baseR4'
)


def create_patient():
    patient = client.resource(
        "Patient",
        identifier=[{"system": "http://clinfhir.com/fhir/NamingSystem/identifier",
                     "value": "11151982"}],
        name=[{"use": "official",
               "text": "Belcher, Bob",
               "family": "Belcher",
               "given": ["Robert"]}],
        gender="male",
        birthDate="1990-01-29"
    )
    patient.save()
    print(patient.id)
    return patient


def create_practitioner():
    practitioner = client.resource(
        "Practitioner",
        name=[{"text": "Victest, Alpha"}],
        active=True
    )
    practitioner.save()
    # practitioner["active""]
    print("Practioner:", practitioner.id)
    return practitioner


def create_schedule(practitionerreference):
    schedule = client.resource(
        "Schedule",
        active=True,
        serviceCategory=[{"coding": [{
            "code": "17",
            "display": "General Practice",
        }],
        }],
        actor=[{"reference": practitionerreference,
                "display": "Victest, Alpha"}],
        planningHorizon=[{"Start": datetime.datetime.now(pytz.utc).isoformat(),
                          "End": datetime.datetime(2022, 12, 31, 23, 59, 59, 0, tzinfo=pytz.utc).isoformat()}]
    )
    schedule.save()
    print("Schedule ID:", schedule.id)
    return schedule


def create_slot(schedule, practitioner, mins):
    slot = client.resource(
        "Slot",
        schedule=[{"reference": schedule.reference}],
        status="free",
        start=datetime.datetime(2022, 2, 4, 12, mins, tzinfo=pytz.utc).isoformat(),
        end=datetime.datetime(2022, 2, 4, 12, mins + 10, tzinfo=pytz.utc).isoformat(),
        serviceCategory=[{"coding": [{
            "code": "17",
            "display": "General Practice",
        }],
        }],
        serviceType=[{"coding": [{
            "code": "17",
            "display": "Immunization",
        }],
        }]
    )
    slot.save()
    print("Slot ID", slot.id)
    return slot


def create_multiple_slots(schedule, practitioner):
    instances = 5
    start_min = 0
    slots = []
    for instance in range(0, instances):
        start_min = instance * 10
        slots.append(create_slot(schedule, practitioner, start_min))


# patient = create_patient()
practitioner = create_practitioner()
schedule = create_schedule(practitioner.reference)
slots = create_multiple_slots(schedule, practitioner)
