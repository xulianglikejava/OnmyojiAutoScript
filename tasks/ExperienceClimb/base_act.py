# This Python file uses the following encoding: utf-8
"""体验服体力爬塔的最小运行流程。"""

import time
from datetime import datetime

from module.exception import TaskEnd
from module.logger import logger
from tasks.Component.GeneralBattle.general_battle import GeneralBattle
from tasks.ExperienceClimb.assets import ExperienceClimbAssets
from tasks.GameUi.game_ui import GameUi
from tasks.GameUi.page import page_battle_result, page_reward


class ExperienceClimbAct(GameUi, GeneralBattle, ExperienceClimbAssets):
    """在用户手动打开的体验服爬塔页面上点击挑战并执行通用战斗。"""

    def _exit_matcher(self):
        """返回受战斗阶段保护的挑战按钮结束判断。"""

        # 挑战按钮可能在点击后的过渡帧短暂残留，交给回调判断可避免首帧误退出。
        return self._is_battle_finished

    def _is_battle_finished(self):
        """仅在通用战斗到达结算或奖励页后，判断挑战按钮是否重新出现。"""

        # 没有先识别到战斗页时，挑战按钮的残留不能代表战斗结束，更不能判定失败。
        context = self._battle_context
        if context is None or context.last_page not in {page_battle_result, page_reward}:
            return False

        # 战斗结算后重新出现挑战按钮，说明上一轮已完整结束；继续沿用这一张图片。
        return self.appear(self.I_ACT_FIRE)

    def run(self):
        """循环识别挑战按钮，点击后交给通用战斗逻辑，直到次数或时间达到上限。"""

        # 体验服只运行体力爬塔，次数和总时长沿用原配置中的 ap_limit、limit_time。
        experience_config = self.config.model.experience_climb
        climb_config = experience_config.general_climb
        battle_config = experience_config.ap_battle_conf
        battle_limit = max(int(climb_config.ap_limit), 0)
        deadline = self.start_time + climb_config.limit_time_v

        logger.hr("Experience climb start", 1)
        while self.current_count < battle_limit and datetime.now() < deadline:
            self.screenshot()

            # 当前页面由用户提前打开；只依赖这一张体验服挑战按钮图，不再识别入口、模式或剩余体力。
            if self.appear_then_click(self.I_ACT_FIRE, interval=1.5):
                logger.info("Experience climb challenge clicked")
                self.run_general_battle(
                    battle_config,
                    battle_key="experience_climb.ap",
                )
                continue

            # 挑战按钮尚未出现在当前帧时短暂等待，避免高频截图和重复点击。
            time.sleep(0.5)

        if self.current_count >= battle_limit:
            logger.info("Experience climb count limit reached")
        else:
            logger.info("Experience climb time limit reached")
        self.set_next_run(task="ExperienceClimb", success=True)
        raise TaskEnd
