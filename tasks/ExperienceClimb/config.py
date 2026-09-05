# This Python file uses the following encoding: utf-8
"""体验服爬塔配置。

体验服与当前爬塔共用同一套配置结构，运行时通过独立任务字段保存配置，
避免正式服和体验服的调度、御魂切换及战斗参数互相覆盖。
"""

from tasks.ActivityShikigami.config import ActivityShikigami


class ExperienceClimb(ActivityShikigami):
    """体验服爬塔配置，字段与当前爬塔保持一致。"""
