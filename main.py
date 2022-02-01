from time import strftime
from fhirpy import SyncFHIRClient
import datetime

# Set Up Variables
SlotID = 2806207
ScheduleID = 2806206
PractitionerID = 2806205
PatientID = 2806193

# Create an instance
client = SyncFHIRClient(
    'http://hapi.fhir.org/baseR4'
)

slot = client.resources('Slot')
schedule = client.resources('Schedule')
slot = slot.search(schedule=ScheduleID, status="free")

print("Searching for available slots...")

slots = slot.fetch()
print("# Start                End                  Service Type")
for index, entry in enumerate(slots):
    print(index, datetime.datetime.fromisoformat(entry.start).strftime('%b-%d-%Y %H:%M %p'),
          datetime.datetime.fromisoformat(entry.end).strftime('%b-%d-%Y %H:%M %p'),
          entry.serviceType[0].coding[0].display)
if slots:
    selection = int(input("Select Entry to book: "))
    appointment = client.resource(
        "Appointment",
        Slot=[{
            "reference": slots[selection].reference
        }],
        status="booked",
        start=slots[selection].start,
        end=slots[selection].end,
        participant=[{
            "actor": [{
                "reference": "Patient/{}".format(PatientID),
                "display": "Belcher, Bob"
            }],
            "status": "accepted",
            "actor": [{
                "reference": "Practitioner/{}".format(PractitionerID),
                "display": "Victest, Alpha"
            }],
            "status": "accepted"
        }],
        reasonCode=[{"text": "To Prevent COVID"}]
    )
    appointment.save()
    slots[selection].status = "busy"
    slots[selection].save()

    print("Appointment booked with Appointment ID {}".format(appointment.id))
    print("Appointment Reason: {}".format(appointment.reasonCode[0].text))
else:
    print("No Available Time Slots")
