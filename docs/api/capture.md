# Capture Endpoint

The capture endpoint is used to send new examples to Hulahoop. It is located at:

```
POST /api/capture/<project_id>/
```

## Authorization

No authorization is required to POST data to the capture endpoint.

## HTTP Methods

Only `POST` method is allowed for the capture endpoint.

## HTTP Headers

The capture endpoint supports only JSON payloads. While not enforced by the endpoint, we recommend submitting the valid MIME type for JSON payloads:

```
Content-Type: application/json
```

## JSON Payload

### Required Attributes

Attributes are simple data that Hulahoop understands to provide the most basic information about examples. These are things like the unique ID of an example or the time when it occurred.

The following attributes are required for all examples:

`attachments`

Required. A non-empty list of files related to the example. Every attachment has the following fields:

```json
{
  "attachments": [
    {
      "url": "...",
      "type": "..."
    }
  ]
}
```

where `url` field specifies the attachment location and acceptable values for `type` are:

- `unknown`
- `image`
- `video`
- `audio`
- `text`

Currently, we support fetching URLs over HTTP or HTTPS. HTTPS is preferred over HTTP, as HTTPS guarantees data integrity, preventing corruption. Make sure that the URL is a direct link to the file you with and that the URL is acceccible to Hulahoop without additional authorization. As Hulahoop does not download and store files from provided URLs, make sure that the the URL will be acceccible in the future.

### Optional Attributes

Additionally, there are several optional values which Hulahoop recognizes and are highly encouraged:

`timestamp`

Optional. Example timestamp in [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) format. Current server date and time will be used if not set.

```json
{
  "timestamp": "2022-06-02T17:41:36Z"
}
```

`fingerprint`

Optional. A string which defines example groupping to issues. Example with the same fingerprint value are groupped to the same issue. Other groupping methods will be used if not set.

```json
{
  "fingerprint": "low-score-predictions"
}
```

`tags`

Optional. A map of tags for this example. Tag key is limited to 30 characters and tag value is limited to 200 characters.

```json
{
  "tags": {
    "key": "value"
  }
}
```

`predictions`

TODO

`annotations`

TODO

`metadata`

Optional. Metadata is useful for storing additional, structured information on an example, especially information that can help you analyse the example or keep track of what context this example corresponds to. Metadata is not used by Hulahoop.

### Response

TODO

## A Working Example

The capture request payload should resemble the following:

```json
{
  "attachments": [
    {
      "url": "https://upload.wikimedia.org/wikipedia/commons/9/98/Girl_twirling_Hula_Hoop%2C_1958.jpg",
      "type": "image"
    }
  ],
  "timestamp": "2022-06-02T17:41:36Z",
  "fingerprint": "hulahoop",
  "tags": [
    {
      "source": "Wikipedia",
      "color": "grayscale",
      "decade": "50s",
      "predicted": "girl"
    }
  ],
  "predictions": {
    "label": "girl",
    "choices": ["girl", "boy"]
  },
  "metadata": {
    "original_url": "https://en.wikipedia.org/wiki/Hula_hoop",
    "year": 1958
  }
}
```
