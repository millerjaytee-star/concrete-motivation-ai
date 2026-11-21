import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { createElement, useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { CommandCurriculum } from "@/components/CommandCurriculum";
import {
  checkCurriculumAnswer,
  curriculumCompletionTitle,
  curriculumLessons,
  curriculumProgress,
  curriculumTracks,
  type CurriculumTrack
} from "@/lib/command-curriculum";
import { siteConfig } from "@/lib/site-config";

const tracks = Object.keys(curriculumTracks) as CurriculumTrack[];

afterEach(cleanup);

describe("financial-literacy curriculum", () => {
  it("covers each topic for every age using the established pillars", () => {
    expect(curriculumLessons.map((lesson) => lesson.title)).toEqual([
      "History of money",
      "Earning and value creation",
      "Saving",
      "Budgeting",
      "Debt and interest",
      "Investing fundamentals",
      "Entrepreneurship",
      "Ownership",
      "Risk",
      "Long-term wealth building",
      "Ethics and financial decisions"
    ]);
    expect(new Set(curriculumLessons.map((lesson) => lesson.pillar))).toEqual(new Set(siteConfig.pillars));
    for (const lesson of curriculumLessons) {
      expect(lesson.educator).toBeTruthy();
      expect(lesson.brick).toBeTruthy();
      for (const track of tracks) {
        const exercise = lesson.exercises[track];
        const correctChoices = exercise.choices.filter((_, choice) => checkCurriculumAnswer(lesson, track, choice)?.correct);
        expect(correctChoices).toHaveLength(1);
        expect(checkCurriculumAnswer(lesson, track, -1)).toBeNull();
        expect(checkCurriculumAnswer(lesson, track, exercise.choices.length)).toBeNull();
      }
    }
  });

  it("counts only unique completed lessons in one learning track", () => {
    const lesson = curriculumLessons[0];
    const records = [
      { title: curriculumCompletionTitle(lesson, "children") },
      { title: curriculumCompletionTitle(lesson, "children") },
      { title: curriculumCompletionTitle(lesson, "adults") },
      { title: "Unknown lesson" }
    ];
    expect(curriculumProgress("children", records)).toBe(1);
    expect(curriculumProgress("teenagers", records)).toBe(0);
    expect(curriculumProgress("adults", records)).toBe(1);
  });

  it("persists a correct answer only, and displays separately saved progress for each track", async () => {
    const save = vi.fn<(record: { title: string; body: string }) => Promise<void>>().mockResolvedValue(undefined);
    function Harness() {
      const [records, setRecords] = useState<{ title: string }[]>([]);
      return createElement(CommandCurriculum, {
        completed: records,
        onComplete: async (record) => {
          await save(record);
          setRecords((previous) => [...previous, record]);
        }
      });
    }

    render(createElement(Harness));
    const choices = screen.getAllByRole("radio");
    fireEvent.click(choices[0]);
    fireEvent.click(screen.getByRole("button", { name: "Check answer" }));
    expect(screen.getByText(/Try again/)).toBeTruthy();
    expect(save).not.toHaveBeenCalled();

    fireEvent.click(choices[1]);
    fireEvent.click(screen.getByRole("button", { name: "Check answer" }));
    await waitFor(() => expect(screen.getByText("Lesson completed.")).toBeTruthy());
    expect(save).toHaveBeenCalledWith({
      title: "History of money · Children",
      body: "Learning track: Children\nPillar: Foundation\nAssessment: correct"
    });
    expect(screen.getByText("1 of 11 lessons completed in Children")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Check answer" }));
    expect(save).toHaveBeenCalledTimes(1);

    fireEvent.change(screen.getByLabelText("Learning track"), { target: { value: "teenagers" } });
    expect(screen.getByText("0 of 11 lessons completed in Teenagers")).toBeTruthy();
    expect(screen.queryByText("Lesson completed.")).toBeNull();
  });

  it("allows completion to be retried after a failed save", async () => {
    const save = vi.fn()
      .mockRejectedValueOnce(new Error("offline"))
      .mockResolvedValueOnce(undefined);

    render(createElement(CommandCurriculum, { onComplete: save }));
    fireEvent.click(screen.getAllByRole("radio")[1]);
    fireEvent.click(screen.getByRole("button", { name: "Check answer" }));
    await waitFor(() => expect(screen.getByRole("alert").textContent).toMatch(/could not be saved/));
    expect(screen.queryByText("Lesson completed.")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "Check answer" }));
    await waitFor(() => expect(screen.getByText("Lesson completed.")).toBeTruthy());
    expect(save).toHaveBeenCalledTimes(2);
  });
});
