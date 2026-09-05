# This Python file uses the following encoding: utf-8
# @author AzurTian
# 体验服任务要求用户手动打开体力爬塔页面，具体流程只保留挑战按钮和通用战斗。
from tasks.ExperienceClimb.base_act import ExperienceClimbAct
from tasks.base_task import BaseTask


class ScriptTask(BaseTask):
    """体验服爬塔任务入口。"""

    def run(self):
        # 不负责进入活动页；用户应在启动任务前手动停留在挑战按钮可见的页面。
        ExperienceClimbAct(self.config, self.device).run()
