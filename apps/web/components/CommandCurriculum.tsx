"use client";

import Link from "next/link";
import * as React from "react";

import {
  checkCurriculumAnswer,
  curriculumCompletionTitle,
  curriculumLessons,
  curriculumProgress,
  curriculumTracks,
  type CurriculumTrack
} from "@/lib/command-curriculum";
import { siteConfig } from "@/lib/site-config";

import styles from "./CommandCurriculum.module.css";

type Completion = { title: string; body: string };

type Props = {
  completed?: readonly { title: string }[];
  onComplete: (result: Completion) => Promise<void>;
};

export function CommandCurriculum({ completed = [], onComplete }: Props) {
  const [track, setTrack] = React.useState<CurriculumTrack>("children");
  const [lessonId, setLessonId] = React.useState(curriculumLessons[0].id);
  const [saving, setSaving] = React.useState(false);
  const lesson = curriculumLessons.find(({ id }) => id === lessonId) ?? curriculumLessons[0];
  const title = curriculumCompletionTitle(lesson, track);
  const progress = curriculumProgress(track, completed);

  async function saveCompletion(result: Completion) {
    setSaving(true);
    try {
      await onComplete(result);
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className={styles.curriculum} aria-label="Financial literacy curriculum">
      <p>{siteConfig.phrase}</p>
      <p className={styles.subtle}>Financial literacy pilot through the Six Pillars and the Daily Brick.</p>
      <div className={styles.selectors}>
        <label htmlFor="curriculum-track">
          Learning track
          <select id="curriculum-track" value={track} disabled={saving} onChange={(event) => {
            const nextTrack = event.target.value;
            if (Object.hasOwn(curriculumTracks, nextTrack)) setTrack(nextTrack as CurriculumTrack);
          }}>
            {Object.entries(curriculumTracks).map(([id, label]) => <option key={id} value={id}>{label}</option>)}
          </select>
        </label>
        <label htmlFor="curriculum-lesson">
          Lesson
          <select id="curriculum-lesson" value={lessonId} disabled={saving} onChange={(event) => setLessonId(event.target.value)}>
            {curriculumLessons.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}
          </select>
        </label>
      </div>
      <label className={styles.progress} htmlFor="curriculum-progress">
        <span>{progress} of {curriculumLessons.length} lessons completed in {curriculumTracks[track]}</span>
        <progress id="curriculum-progress" value={progress} max={curriculumLessons.length} />
      </label>
      <article className={styles.lesson}>
        <p className={styles.pillar}>{lesson.pillar}</p>
        <h3>{lesson.title}</h3>
        <p>{lesson.introduction}</p>
        <LessonExercise
          key={title}
          lesson={lesson}
          track={track}
          title={title}
          completed={completed.some((record) => record.title === title)}
          saving={saving}
          onComplete={saveCompletion}
        />
        <div className={styles.brick}>
          <strong>Daily Brick</strong>
          <p>{lesson.brick}</p>
        </div>
        <details className={styles.educator}>
          <summary>Educator notes</summary>
          <p><strong>Learning outcome</strong> {lesson.outcome}</p>
          <p>{lesson.educator}</p>
          <p>Use fictional amounts and scenarios. Ask learners to explain their choice before they try the Daily Brick.</p>
          <ul>
            <li><Link href="/daily-brick">Daily Brick guide</Link></li>
            <li><Link href="/foundation-challenge">Seven-Day Foundation Challenge</Link></li>
            <li><a href="https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/">CFPB youth financial education resources</a></li>
            <li><a href="https://www.investor.gov/introduction-investing">Investor.gov investing fundamentals</a></li>
          </ul>
        </details>
      </article>
    </section>
  );
}

function LessonExercise({ lesson, track, title, completed, saving, onComplete }: {
  lesson: (typeof curriculumLessons)[number];
  track: CurriculumTrack;
  title: string;
  completed: boolean;
  saving: boolean;
  onComplete: Props["onComplete"];
}) {
  const [choice, setChoice] = React.useState<number | null>(null);
  const [checked, setChecked] = React.useState<number | null>(null);
  const [saved, setSaved] = React.useState(false);
  const [saveError, setSaveError] = React.useState(false);
  const inFlight = React.useRef(false);
  const result = checked === null ? null : checkCurriculumAnswer(lesson, track, checked);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (choice === null || inFlight.current) return;
    const assessment = checkCurriculumAnswer(lesson, track, choice);
    if (!assessment) return;
    setChecked(choice);
    setSaveError(false);
    if (!assessment.correct || completed || saved) return;
    inFlight.current = true;
    try {
      await onComplete({
        title,
        body: [`Learning track: ${curriculumTracks[track]}`, `Pillar: ${lesson.pillar}`, "Assessment: correct"].join("\n")
      });
      setSaved(true);
    } catch {
      setSaveError(true);
    } finally {
      inFlight.current = false;
    }
  }

  return (
    <form className={styles.exercise} onSubmit={submit}>
      <fieldset disabled={saving}>
        <legend>{lesson.exercises[track].scenario}</legend>
        {lesson.exercises[track].choices.map((answer, index) => (
          <label key={answer}>
            <input
              type="radio"
              name="curriculum-answer"
              checked={choice === index}
              required
              onChange={() => {
                setChoice(index);
                setChecked(null);
                setSaveError(false);
              }}
            />
            {answer}
          </label>
        ))}
      </fieldset>
      <button type="submit" disabled={choice === null || saving}>
        {saving ? "Saving progress…" : "Check answer"}
      </button>
      <div aria-live="polite">
        {result?.correct && <p><strong>Correct.</strong> {result.explanation}</p>}
        {result && !result.correct && <p>Try again. {result.explanation}</p>}
        {(saved || completed) && <p>Lesson completed.</p>}
        {saveError && <p role="alert">Progress could not be saved. Check the answer again to retry.</p>}
      </div>
    </form>
  );
}
