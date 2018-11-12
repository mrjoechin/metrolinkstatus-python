# Metrolink Status
This little script will grab scheduled stops at stations specified in the config area and push the status of those trains to slack.

To use:
* Update the Following
  * `slackWebhookURL` string
  * `stations` array
* To print messages turn on debugging
  * set `debug` to *True* 
