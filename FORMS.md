# Website enquiry forms

Every enquiry form on the site is delivered to **hello@breathetherm.co.uk**.
The site is static (GitHub Pages), so there is no server to receive a POST: the
browser sends the form to Web3Forms, which emails it on.

## Switch on automatic delivery (one step)

Until a key is set, a completed form opens the visitor's email app with every
field already filled in, addressed to hello@breathetherm.co.uk. Nothing is lost,
but the visitor has to press send.

1. Go to https://web3forms.com and enter **hello@breathetherm.co.uk**.
2. Copy the access key from the email it sends back.
3. Paste it into `LEAD.accessKey` in `main.js` (search for `accessKey`).

That is the whole change. The key is a public identifier, safe to ship in the
page source. Free plan: 250 submissions a month, spam filtering, no server.

If a send ever fails, the form still falls back to the pre-filled email, so a
lead is never silently dropped.

## Forms that exist

| Page | Form | `data-form-name` |
| --- | --- | --- |
| `/` and `/contact/` | Free assessment (two steps: who you are, then details) | Free assessment request |
| `/will-it-work/` | Quiz capture, includes the seven answers | Will it work — quiz answers |
| `/for-installers/` | Installer network application | Installer network application |
| `/for-architects/` | Technical pack request | Technical pack request |

## Adding another form

Mark the form and point it at a success panel:

```html
<form class="lead-form" data-lead-form data-form-name="Datasheet request"
      data-success="datasheetSuccess" novalidate>
  <input type="checkbox" name="botcheck" class="form-honey" tabindex="-1"
         autocomplete="off" aria-hidden="true">
  <div class="form-group">
    <label for="d-email">Email</label>
    <input class="form-input" id="d-email" name="email" type="email" required>
  </div>
  <button type="submit" class="btn btn-primary">Send</button>
</form>
<div class="form-success" id="datasheetSuccess" hidden>
  <h3>Thanks — we'll be in touch.</h3>
</div>
```

`main.js` handles validation, the sending state, the success panel and the email
fallback. Field names become the labels in the email. The page path, form name
and a timestamp are added automatically.

Optional attributes:

- `data-fallback-link` / `data-fallback-label`: an extra link on the fallback
  panel, such as the quiz's "See your answer anyway".
- `data-fallback-auto="false"`: do not open the visitor's email app on failure
  (used by the quiz, where the result matters more than the email).

## Using a different provider

Change `LEAD.endpoint` and the request body in `sendLead()`. Formspree, Basin
and Formsubmit all work the same way; Web3Forms was chosen because its free
plan has no per-form setup and includes spam filtering.

## Privacy

The forms carry a line saying the details are used only to reply. The privacy
page (`/privacy/`) is still a placeholder, and a live privacy notice should name
Web3Forms as the processor that carries the enquiry by email, and say how long
enquiries are kept.
