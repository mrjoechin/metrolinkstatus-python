# Metrolink Status
This little script will grab scheduled stops at stations specified in the config area and push the status of those trains to slack.

To use:
* Create a Slack app at https://api.slack.com/apps
  * Add a Webhook, read up here https://api.slack.com/incoming-webhooks
* Update the Following
  * `slackWebhookURL` string
  * `stations` array
* To print messages turn on debugging
  * set `debug` to *True* 
