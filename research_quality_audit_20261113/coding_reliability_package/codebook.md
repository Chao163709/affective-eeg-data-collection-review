# Codebook — Affect-EEG Corpus Coding Scheme (AECS v1.0.0)

*A document-based coding scheme for released affect-EEG corpora. It separates what a corpus is released for from how that label was produced, so that two corpora with the same nominal task can be recognised as supporting different analyses.*

## Principles

- Code from documents only. Do not infer a value from general practice.
- Absence of a statement is not a negative finding.
- cannot judge is a valid value and is more informative than a guess.

## Fields

### `corpus` — Corpus identifier
- Type: `string`; required: True
- Note: Short name used in the release or its descriptor.

### `released_target` — Label the corpus is released for
- Type: `enum`; required: True
- Values: `assigned`, `self-report`, `observer`, `mixed`, `cannot judge`
  - `assigned`: One category per stimulus unit, identical for every participant, and this is the corpus's main task.
  - `self-report`: Each participant's own rating is the released target.
  - `observer`: Labels are scores that external raters gave to participants.
  - `mixed`: Labels for the same cell come from more than one source with no single main task.
  - `cannot judge`: The document does not state it.
- Note: Ask what the distributed label file contains, not what was collected during the session.

### `additional_stream` — Second annotation source released alongside the target
- Type: `enum`; required: True
- Values: `none`, `ratings`, `feedback`, `observer`, `mixed`, `cannot judge`
  - `none`: No second stream is released.
  - `ratings`: Participant ratings are released on top of an assigned target.
  - `feedback`: A participant-level score that is not an affect rating, for example an induction-success score.
  - `observer`: An observer annotation released alongside another target.
  - `mixed`: Streams of more than one kind appear together.
  - `cannot judge`: The document does not state it.
- NOT a stream (do not code these as annotation sources): game identity; an experimental condition fixed by design; song or clip category; stimulus metadata such as duration or language
- Note: The test is whether a different role labels the same cell.

### `ratings_per_stimulus` — How many ratings one participant gives per stimulus
- Type: `enum`; required: True
- Values: `one`, `multiple`, `time_resolved`, `session_level`, `cannot judge`
  - `one`: A single rating per presented stimulus.
  - `multiple`: Several ratings per stimulus; record the number in notes.
  - `time_resolved`: An annotation at fixed intervals inside the exposure; record the interval in notes.
  - `session_level`: One annotation covering a whole session.
  - `cannot judge`: The document does not state it.
- Note: A post-session summary score is session_level, not time_resolved. Only an in-exposure interval makes a label time resolved.

### `stimulus_unit` — What one rating refers to
- Type: `enum`; required: True
- Values: `clip`, `trial`, `song`, `excerpt`, `game`, `conversation`, `period`, `exchange`, `other`, `cannot judge`
  - `clip`: One video or film clip.
  - `trial`: One experimental trial, possibly containing several sub-events.
  - `song`: One music track.
  - `excerpt`: One excerpt of a longer musical or audiovisual item.
  - `game`: One game session or game condition.
  - `conversation`: One dialogue as a whole.
  - `period`: A defined time block, such as a pre- or post-task period.
  - `exchange`: One turn or exchange in an interaction.
  - `other`: None of the above; describe it in notes.
  - `cannot judge`: The document does not state it.
- Note: When a release describes conditions rather than items, the unit is the condition, and the corpus cannot be pooled with clip-level corpora without a conversion rule.

### `stimuli_shared` — Did all participants see the same stimuli?
- Type: `enum`; required: True
- Values: `yes`, `no`, `cannot judge`
  - `yes`: The same material was presented to every participant.
  - `no`: The document states that material differed between participants, for example own dialogues or participant-chosen media.
  - `cannot judge`: The document is silent.
- Note: Silence is cannot judge, never no.

### `protocol_records_self_report` — Did the protocol collect a participant rating?
- Type: `enum`; required: True
- Values: `yes`, `no`, `not established`, `cannot judge`
  - `yes`: The procedure includes a participant rating.
  - `no`: The document states that no participant rating was collected.
  - `not established`: The procedure is described but whether participants rated anything is not stated.
  - `cannot judge`: The document does not describe the procedure.
- Note: not established requires a description of the procedure. If there is no procedure description at all, use cannot judge.

### `release_description` — Does the release description mention participant-rating files?
- Type: `enum`; required: True
- Values: `explicitly describes`, `does not mention`, `not inspected`, `cannot judge`
  - `explicitly describes`: The release description names or lists participant-rating files.
  - `does not mention`: The description was read and contains no such mention.
  - `not inspected`: The description could not be reached.
  - `cannot judge`: The description was reached but is too vague to decide.
- Note: does not mention never means the file does not exist. It records what the description says, not what the package holds.

### `n_subjects` — Participant count
- Type: `int_or_tbd`; required: True
- Note: Record the released or analysed count. If recruited, recorded and analysed counts differ, record the released count and put the others in notes.

### `n_stimuli` — Stimulus count
- Type: `int_or_tbd`; required: True
- Note: When the release describes conditions rather than items, record TBD and state the condition structure in notes.

### `notes` — Evidence note
- Type: `string`; required: True
- Note: Which document was read and which sentence decided the values. This is the only defence of the coding.

### `cannot_judge_fields` — Fields answered with cannot judge
- Type: `list`; required: False
- Note: Must list every field whose value is cannot judge, so that the share of undetermined fields can be counted.

### `source_used` — Document actually used
- Type: `url_or_doi`; required: True

### `date` — Coding date
- Type: `iso_date`; required: True
