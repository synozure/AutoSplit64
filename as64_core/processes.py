import time

import cv2
import numpy as np

import as64_core

from as64_common.resource_utils import resource_path

from as64_core import config
from as64_core.image_utils import is_black
from as64_core.processing import Process, Signal


class ProcessRunStart(Process):
    FADEOUT = Signal("PRS_FADEOUT")
    START = Signal("PRS_START")

    def __init__(self):
        super().__init__()

    def execute(self):
        if as64_core.fade_status in (as64_core.FADEOUT_COMPLETE, as64_core.FADEOUT_PARTIAL):
            return ProcessRunStart.FADEOUT
        else:
            if as64_core.split_index() > 0:
                prev_split_star = as64_core.route.splits[as64_core.split_index()-1].star_count
            else:
                prev_split_star = as64_core.route.initial_star

            if as64_core.prediction_info.prediction == as64_core.star_count and as64_core.prediction_info.probability > config.get("thresholds", "probability_threshold"):
                as64_core.enable_fade_count(True)
                return ProcessRunStart.START
            elif prev_split_star <= as64_core.prediction_info.prediction <= as64_core.current_split().star_count and as64_core.prediction_info.probability > config.get("thresholds", "probability_threshold"):
                as64_core.enable_fade_count(True)
                as64_core.set_star_count(as64_core.prediction_info.prediction)
                return ProcessRunStart.START

        return Process.LOOP

    def on_transition(self):
        print("PROCESS RUN START")
        as64_core.enable_fade_count(False)
        as64_core.fps = 6

        super().on_transition()


class ProcessStarCount(Process):
    FADEOUT = Signal("PSC_FADEOUT")
    FADEIN = Signal("PSC_FADEIN")

    def __init__(self):
        super().__init__()

    def execute(self):
        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessStarCount.FADEOUT

        if as64_core.fade_status in (as64_core.FADEIN_PARTIAL, as64_core.FADEIN_COMPLETE):
            return ProcessStarCount.FADEIN

        return Process.LOOP

    def on_transition(self):
        print("PROCESS STAR COUNT")
        as64_core.fps = config.get("advanced", "star_process_frame_rate")
        as64_core.enable_predictions(True)

        super().on_transition()


class ProcessFadein(Process):
    COMPLETE = Signal("PFI_COMPLETE")

    def __init__(self):
        super().__init__()

    def execute(self):
        if as64_core.incoming_split() and as64_core.fade_status == as64_core.FADEIN_COMPLETE:
            as64_core.split()

        if as64_core.fade_status == as64_core.FADEIN_PARTIAL:
            return Process.LOOP
        else:
            return ProcessFadein.COMPLETE

    def on_transition(self):
        print("PROCESS FADEIN")
        as64_core.fps = 29.97
        as64_core.enable_predictions(False)
        as64_core.fadein()

        super().on_transition()


class ProcessFadeout(Process):
    RESET = Signal("PFO_RESET")
    COMPLETE = Signal("PFO_COMPLETE")

    def __init__(self):
        super().__init__()

        self._split_occurred = False

        self._fps = config.get("advanced", "fadeout_process_frame_rate")
        self._reset_threshold = config.get("thresholds", "reset_threshold")
        self._black_threshold = config.get("thresholds", "black_threshold")

        _, _, reset_width, reset_height = as64_core.get_region_rect(as64_core.RESET_REGION)
        self._reset_template = cv2.resize(cv2.imread(resource_path(config.get("advanced", "reset_frame_one"))), (reset_width, reset_height), interpolation=cv2.INTER_AREA)
        self._reset_template_2 = cv2.resize(cv2.imread(resource_path(config.get("advanced", "reset_frame_two"))), (reset_width, reset_height), interpolation=cv2.INTER_AREA)

    def execute(self):
        reset_region = as64_core.get_region(as64_core.RESET_REGION)

        # If centre of screen is black, and the current split conditions are met, trigger split
        if is_black(reset_region, self._black_threshold) and as64_core.incoming_split():
            as64_core.split()
            self._split_occurred = True

        # Check for a match against the reset_template (SM64 logo)
        match = cv2.minMaxLoc(cv2.matchTemplate(reset_region,
                                                self._reset_template,
                                                cv2.TM_SQDIFF_NORMED))[0]

        if match < self._reset_threshold:
            # If this fadeout triggered a split, undo before reset
            if self._split_occurred:
                as64_core.undo()
            as64_core.enable_predictions(True)
            return ProcessFadeout.RESET
        else:
            match2 = cv2.minMaxLoc(cv2.matchTemplate(reset_region,
                                                     self._reset_template_2,
                                                     cv2.TM_SQDIFF_NORMED))[0]

            if match2 < config.get("thresholds", "reset_threshold"):
                # If this fadeout triggered a split, undo before reset
                if self._split_occurred:
                    as64_core.undo()
                as64_core.enable_predictions(True)
                return ProcessFadeout.RESET

        # If both star count, and life count are still black, reprocess fadeout, otherwise fadeout completed
        if as64_core.fade_status in (as64_core.FADEOUT_COMPLETE, as64_core.FADEOUT_PARTIAL):
            return Process.LOOP
        else:
            as64_core.enable_predictions(True)
            return ProcessFadeout.COMPLETE

    def on_transition(self):
        print("PROCESS FADEOUT")
        as64_core.fps = self._fps
        self._split_occurred = False
        as64_core.enable_predictions(False)
        super().on_transition()


class ProcessPostFadeout(Process):
    FADEOUT = Signal("PPF_FADEOUT")
    FADEIN = Signal("PPF_FADEIN")
    FLASH = Signal("PPF_FLASH")
    COMPLETE = Signal("PPF_COMPLETE")

    def __init__(self):
        super().__init__()

    def execute(self):
        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessPostFadeout.FADEOUT

        if as64_core.fade_status in (as64_core.FADEIN_PARTIAL, as64_core.FADEIN_COMPLETE):
            return ProcessPostFadeout.FADEIN

        if as64_core.prediction_info.prediction in (121, 122) and self.loop_time() > 1:
            return ProcessPostFadeout.FLASH

        if self.loop_time() < 6:
            return Process.LOOP
        else:
            return ProcessPostFadeout.COMPLETE

    def on_transition(self):
        print("PROCESS POST FADEOUT")

        as64_core.enable_predictions(True)
        as64_core.fps = 15

        super().on_transition()


class ProcessFlashCheck(Process):
    FADEOUT = Signal("PPF_FADEOUT")
    FADEIN = Signal("PPF_FADEIN")
    COMPLETE = Signal("PFC_COMPLETE")

    def __init__(self):
        super().__init__()

        self._running_total = 0
        self._prev_prediction = 0
        self._flash_count = 0

    def execute(self):
        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessFlashCheck.FADEOUT

        if as64_core.fade_status in (as64_core.FADEIN_PARTIAL, as64_core.FADEIN_COMPLETE):
            return ProcessFlashCheck.FADEIN

        if as64_core.prediction_info.prediction in (121, 122):
            normalized_prediction = 1
        else:
            normalized_prediction = -1

        if normalized_prediction == self._prev_prediction * -1:
            self._flash_count += 1

        self._running_total += normalized_prediction
        self._prev_prediction = normalized_prediction

        if -10 < self._running_total < 10 and self._flash_count >= 4:
            print("Flash Detected!")
            print("Running Total:", self._running_total, "Flash Count:", self._flash_count)
            if time.time() - as64_core.collection_time > 15:
                print("Increment Star from Flash!")
                as64_core.set_star_count(as64_core.star_count + 1)

                if as64_core.current_split().star_count == as64_core.star_count:

                    if as64_core.current_split().on_fadeout == 1:
                        as64_core.skip()
                    else:
                        as64_core.fadeout_count += 1

            return ProcessFlashCheck.COMPLETE

        if self.loop_time() < 2:
            return Process.LOOP
        else:
            return ProcessFlashCheck.COMPLETE

    def on_transition(self):
        print("PROCESS FLASH CHECK")

        as64_core.fps = 29.97
        as64_core.enable_predictions(True)
        self._running_total = 0
        self._flash_count = 0
        self._prev_prediction = 0

        super().on_transition()


class ProcessReset(Process):
    RESET = Signal("PR_RESET")

    def __init__(self,):
        super().__init__()
        self._restart_split_delay = config.get("advanced", "restart_split_delay")

    def execute(self):
        if not config.get("general", "srl_mode"):
            as64_core.reset()
            time.sleep(self._restart_split_delay)
            as64_core.split()
            as64_core.enable_fade_count(False)
            as64_core.star_count = as64_core.route.initial_star
        return ProcessReset.RESET

    def on_transition(self):
        print("PROCESS RESET")

        super().on_transition()


class ProcessFinalStageEntry(Process):
    ENTERED = Signal("PFSE_ENTERED")
    FADEOUT = Signal("PFSE_FADEOUT")

    def __init__(self,):
        super().__init__()

        self.bowser_lower_bound = config.get("split_final_star", "stage_lower_bound")
        self.bowser_upper_bound = config.get("split_final_star", "stage_upper_bound")

    def execute(self):
        no_hud = as64_core.get_region(as64_core.NO_HUD_REGION)

        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessFinalStageEntry.FADEOUT

        lower = np.array(self.bowser_lower_bound, dtype="uint8")
        upper = np.array(self.bowser_upper_bound, dtype="uint8")

        star_mask = cv2.inRange(no_hud, lower, upper)
        output = cv2.bitwise_and(no_hud, no_hud, mask=star_mask)

        if not is_black(output, 0.1, 0.9):
            return ProcessFinalStageEntry.ENTERED
        else:
            return Process.LOOP

    def on_transition(self):
        print("PROCESS FINAL STAGE ENTRY")

        as64_core.fps = 10

        super().on_transition()


class ProcessFinalStarSpawn(Process):
    SPAWNED = Signal("PFSS_SPAWNED")
    FADEOUT = Signal("PFSS_FADEOUT")

    def __init__(self):
        super().__init__()
        self._iteration_value = {0: 1, 1: 4, 2: 1}
        self._looping_iteration = 0

        # TODO: Change lower bound to 0, 190, 190. This fixes Yales problem, however may make it not work correctly for other people
        # So instead maybe keep at 0, 180, 180, and just advise to use the new values in settings
        self.star_lower_bound = config.get("split_final_star", "star_lower_bound")
        self.star_upper_bound = config.get("split_final_star", "star_upper_bound")

    def execute(self):
        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessFinalStarSpawn.FADEOUT

        if self._star_visible() and self.loop_time() > 30:
            if self._looping_iteration == len(self._iteration_value):
                print("spawned :)")
                return ProcessFinalStarSpawn.SPAWNED
            else:
                try:
                    print("iter", self._looping_iteration)
                    time.sleep(self._iteration_value[self._looping_iteration])
                except IndexError:
                    pass

            self._looping_iteration += 1

            return Process.LOOP
        else:
            self._looping_iteration = 0

        return Process.LOOP

    def on_transition(self):
        print("PROCESS FINAL STAR SPAWN")
        as64_core.fps = 29.97
        self._looping_iteration = 0

        super().on_transition()

    def _star_visible(self, threshold=0.999):
        no_hud = as64_core.get_region(as64_core.NO_HUD_REGION)

        lower = np.array(self.star_lower_bound, dtype="uint8")
        upper = np.array(self.star_upper_bound, dtype="uint8")

        star_mask = cv2.inRange(no_hud, lower, upper)
        output = cv2.bitwise_and(no_hud, no_hud, mask=star_mask)

        return not is_black(output, 0.1, threshold)


class ProcessFinalStarGrab(Process):
    COMPLETE = Signal("PFSG_COMPLETE")
    FADEOUT = Signal("PFSG_FADEOUT")

    def __init__(self):
        super().__init__()

        self.star_lower_bound = config.get("split_final_star", "star_lower_bound")
        self.star_upper_bound = config.get("split_final_star", "star_upper_bound")

    def execute(self):
        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessFinalStageEntry.FADEOUT

        if not self._star_visible():
            print("Grabbed!")
            as64_core.split()
            return ProcessFinalStarGrab.COMPLETE

        return Process.LOOP

    def on_transition(self):
        print("PROCESS FINAL STAR GRAB")

        as64_core.fps = 29.97

        super().on_transition()

    def _star_visible(self, threshold=0.999):
        no_hud = as64_core.get_region(as64_core.NO_HUD_REGION)

        lower = np.array(self.star_lower_bound, dtype="uint8")
        upper = np.array(self.star_upper_bound, dtype="uint8")

        star_mask = cv2.inRange(no_hud, lower, upper)
        output = cv2.bitwise_and(no_hud, no_hud, mask=star_mask)

        return not is_black(output, 0.1, threshold)


class ProcessFindDDDPortal(Process):
    FOUND = Signal("PFDP_FOUND")
    FADEOUT = Signal("PFDP_FADEOUT")

    def __init__(self,):
        super().__init__()

        self.portal_lower_bound = config.get("split_ddd_enter", "portal_lower_bound")
        self.portal_upper_bound = config.get("split_ddd_enter", "portal_upper_bound")

    def execute(self):
        no_hud = as64_core.get_region(as64_core.GAME_REGION)

        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessFindDDDPortal.FADEOUT

        lower = np.array(self.portal_lower_bound, dtype="uint8")
        upper = np.array(self.portal_upper_bound, dtype="uint8")

        portal_mask = cv2.inRange(no_hud, lower, upper)
        output = cv2.bitwise_and(no_hud, no_hud, mask=portal_mask)

        if not is_black(output, 0.1, 0.99):
            return ProcessFindDDDPortal.FOUND
        else:
            return Process.LOOP

    def on_transition(self):
        print("PROCESS FIND DDD PORTAL")
        as64_core.fps = 10

        super().on_transition()


class ProcessDDDEntry(Process):
    ENTERED = Signal("PDE_ENTERED")
    FADEOUT = Signal("PDE_FADEOUT")

    def __init__(self,):
        super().__init__()

        self.lower_bound = np.array(config.get("split_ddd_enter", "hat_lower_bound"), dtype="uint8")
        self.upper_bound = np.array(config.get("split_ddd_enter", "hat_upper_bound"), dtype="uint8")

    def execute(self):
        no_hud = as64_core.get_region(as64_core.NO_HUD_REGION)

        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessDDDEntry.FADEOUT

        if not cv2.inRange(no_hud, self.lower_bound, self.upper_bound).any():
            as64_core.split()
            return ProcessDDDEntry.ENTERED
        else:
            return Process.LOOP

    def on_transition(self):
        print("PROCESS DDD ENTRY")
        as64_core.fps = 10

        super().on_transition()


class ProcessIdle(Process):
    FADEOUT = Signal("PDE_FADEOUT")

    def __init__(self,):
        super().__init__()

    def execute(self):
        if as64_core.fade_status in (as64_core.FADEOUT_PARTIAL, as64_core.FADEOUT_COMPLETE):
            return ProcessIdle.FADEOUT

        return Process.LOOP

    def on_transition(self):
        as64_core.enable_predictions(False)
        as64_core.fps = 10
        super().on_transition()
