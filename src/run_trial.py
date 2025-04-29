from psyflow import StimUnit
import random
from functools import partial
from psychopy.visual import TextStim
def run_trial(win, kb, settings, condition, stim_bank, trigger_sender, trigger_bank):
    """
    Run a single BART trial:
    fixation → ballon + pump + feedback
    """
    trial_data = {"condition": condition}
    make_unit = partial(StimUnit, win=win, triggersender=trigger_sender)
    continue_pump = True
    pump_count    = 0
    score_bank    = getattr(settings, f"{condition}_delta")
    delta        = getattr(settings, f"{condition}_delta")
    max_pumps    = getattr(settings, f"{condition}_max_pumps")
    initial_scale  = settings.initial_balloon_scale    # e.g. 0.2
    max_scale      = settings.max_balloon_scale        # e.g. 1.8
    balloon_base_deg = settings.balloon_size_deg        # e.g., [4, 5]
    size_step     = (max_scale - initial_scale) / max_pumps
    
    make_unit(unit_label="fixation")\
    .add_stim(stim_bank.get('fixation'))\
    .show(duration=settings.fixation_duration,
          onset_trigger=trigger_bank.get('fixation_onset'))\
    .to_dict(trial_data)

    while continue_pump:
        
        
        current_scale = initial_scale + pump_count * size_step
        balloon_size = [current_scale * balloon_base_deg[0],
                        current_scale * balloon_base_deg[1]]
            # --- 1) Show balloon & capture one response ---
        balloon = make_unit(unit_label=f"pump_{pump_count}") \
                .add_stim(stim_bank.rebuild(f"{condition}_balloon", size=balloon_size)) \
                .add_stim(TextStim(win,text=f'+{score_bank}', pos=[0,-3],color='black'))\
                .capture_response(
                    keys=[settings.pump_key, settings.cash_key],
                    correct_keys=[],               # not used here
                    duration=settings.balloon_duration,
                    onset_trigger=trigger_bank.get(f"{condition}_balloon_onset"),
                    response_trigger={settings.pump_key: trigger_bank.get(f"{condition}_pump_press"),
                                      settings.cash_key: trigger_bank.get(f"{condition}_cash_press")},
                    timeout_trigger=trigger_bank.get(f"{condition}_balloon_onset"),
                    terminate_on_response=True     # end this unit on any key
                ).to_dict(trial_data)
        response = balloon.get_state('response', None)

        if response == settings.pump_key:
            # they pumped!
            #  a) check for pop
            if random.random() < 1.0 / (max_pumps - pump_count + 1):
                # balloon pops
                pop=make_unit(unit_label=f"pop")\
                    .add_stim(stim_bank.get(f"{condition}_pop"))\
                    .add_stim(stim_bank.get("pop_sound"))\
                    .show(duration=settings.response_feedback_duration,
                          onset_trigger=trigger_bank.get(f"{condition}_pop"))\
                    .to_dict(trial_data)
                fb_type = "pop"
                continue_pump = False
                fb_score = 0
            else:# survied and grow and add money
                continue_pump = True
                pump_count += 1
                score_bank += delta
        elif response == settings.cash_key: # cash out
             make_unit(unit_label=f"case") \
                .add_stim(stim_bank.get('cash_screen')) \
                .add_stim(stim_bank.get("cash_sound"))\
                .show(duration=settings.response_feedback_duration,
                      onset_trigger=trigger_bank.get(f"{condition}_cash"))\
                .to_dict(trial_data)
             fb_type = "cash"
             continue_pump = False
             fb_score = score_bank
        else: # no resposne
            make_unit(unit_label='timeout')\
            .add_stim(stim_bank.get('timeout_screen'))\
            .show(duration=settings.response_feedback_duration,
                  onset_trigger=trigger_bank.get(f"{condition}_timeout"))\
             .to_dict(trial_data)
            continue_pump = False
            fb_type = "timeout"
            fb_score = 0

    fb_stim = 'win_feedback' if fb_type == "cash" else 'lose_feedback'
    feedback = make_unit (unit_label='feedback') \
                .add_stim(stim_bank.get_and_format(fb_stim, fb_score=fb_score))\
                .show(duration=settings.feedback_duration,
                        onset_trigger=trigger_bank.get('feedback_onset'))
    feedback.set_state(fb_type=fb_type,
                        fb_score=fb_score)
    feedback.to_dict(trial_data)
    return trial_data
            



  