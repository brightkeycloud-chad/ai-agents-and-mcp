On-call currently has to open the console to record an incident, which is slow
and easy to get wrong at three in the morning. This adds an endpoint so it can
be done from the runbook.

## What it does

`POST /api/incidents` takes a service, a status and a message. It writes the
incident, updates the service's current status to match so the board and the
incident log agree, and returns the number of incidents that service now has.

```bash
curl -X POST https://status.awsf.brightkey.cloud/api/incidents \
  -H 'content-type: application/json' \
  -d '{"service_id": "payments", "status": "degraded", "message": "Elevated latency on checkout."}'
```

It also adds an `outage` status, for a service that is gone entirely rather
than merely degraded. `down` felt wrong for a total outage and we have been
using the two interchangeably in Slack.

## Notes

- The write and the status update happen together, so the board cannot drift
  from the incident log.
- Service ids are checked before anything is written.
- The existing suite passes.
