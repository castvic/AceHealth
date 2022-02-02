from time import strftime
from fhirpy import SyncFHIRClient
import datetime

# Set Up Variables
scheduleID = 2806855
practitionerID = 2806854
patientID = 2806193

# Create a client instance
client = SyncFHIRClient(
    'http://hapi.fhir.org/baseR4'
)

# Create an instance of the resource and search for
# TODO Add sort and increase number returned
slot = client.resources('Slot')
slot = slot.search(schedule=scheduleID, status="free")

# Let User know we are searching for available slots and perform search
print("Searching for available slots...")
slots = slot.fetch()

# Let User know of available slots
print("# Start                End                  Service Type")
for index, entry in enumerate(slots):
    print(index, datetime.datetime.fromisoformat(entry.start).strftime('%b-%d-%Y %H:%M %p'),
          datetime.datetime.fromisoformat(entry.end).strftime('%b-%d-%Y %H:%M %p'),
          entry.serviceType[0].coding[0].display)

# Check to make sure we have entries available to us and if so prompt user to select
# an available Date Time/Service and provide a reason for the visit
if slots:
    # TODO Add better error handling
    selection = int(input("Select Entry to book: "))
    reason = input("Enter Reason for Visit: ")
    appointment = client.resource(
        "Appointment",
        Slot=[{
            "reference": slots[selection].reference
        }],
        status="booked",
        serviceCategory=[{"coding": [{
            "code": "17",
            "display": "General Practice",
        }]
        }],
        start=slots[selection].start,
        end=slots[selection].end,
        participant=[{
            "actor": [{
                "reference": "Patient/{}".format(patientID),
                "display": "Belcher, Bob"
            }],
            "status": "accepted",
            "actor": [{
                "reference": "Practitioner/{}".format(practitionerID),
                "display": "Victest, Alpha"
            }],
            "status": "accepted"
        }],
        reasonCode=[{"text": reason}]
    )
    appointment.save()
    slots[selection].status = "busy"
    slots[selection].save()

    print("Appointment booked with Appointment ID {}".format(appointment.id))
    print("Appointment Reason: {}".format(appointment.reasonCode[0].text))
else:
    print("No Available Time Slots")
