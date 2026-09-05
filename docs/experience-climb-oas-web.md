# 体验服爬塔与 OAS Web 标注操作手册

本文对应任务 `ExperienceClimb`。当前实现只处理体验服体力爬塔的挑战按钮，要求启动任务前由用户手动进入挑战按钮可见的页面。

## 一、当前实际逻辑

```text
用户手动进入体验服体力爬塔页面
    -> 识别 act_fire 挑战按钮
    -> 点击挑战
    -> 调用通用战斗逻辑
    -> 战斗结算后再次识别 act_fire
    -> 继续下一轮
```

体验服任务不再负责以下内容：

- 从庭院进入活动。
- 识别或切换门票、体力、100 体、Boss 模式。
- OCR 读取剩余体力、门票或挑战次数。
- 自动切换御魂、锁定阵容或处理活动专属弹窗。
- 大富翁、伪神、Boss 等活动分支。

体验服任务目录中只保留一条自定义图片规则：

```text
tasks/ExperienceClimb/as/image.json
    -> itemName: act_fire
    -> 图片文件: tasks/ExperienceClimb/as/as_act_fire.png
    -> 代码属性: ExperienceClimbAssets.I_ACT_FIRE
```

通用战斗页面仍使用 OAS 公共战斗资源，因此不需要为准备页、战斗页、结算页重新截图。

## 二、准备运行环境

仓库根目录：

```text
D:\workspace\yys-helper\OnmyojiAutoScript
```

### 1. 启动 OAS Web

在 PyCharm Terminal 或 PowerShell 执行：

```powershell
cd D:\workspace\yys-helper\OnmyojiAutoScript
python server.py --port 22270
```

浏览器打开：

```text
http://127.0.0.1:22270/tool/annotator
```

如果项目使用的 Python 不是系统默认 Python，请把命令中的 `python` 换成 PyCharm 当前解释器的完整路径。

### 2. 准备游戏画面

1. 启动体验服模拟器并登录账号。
2. 保持 OAS 实际运行时使用的分辨率和窗口比例；当前规则按 `1280x720` 设计。
3. 手动进入体验服的体力爬塔页面。
4. 确认画面上能看到“发现挑战/挑战”按钮。
5. 不要让鼠标、通知、悬浮窗遮挡按钮。

## 三、用 OAS Web 截取新的挑战按钮图片

### A. 连接模拟器并截取页面

1. 在 OAS Web 左侧选择“模拟器画面”。
2. “脚本配置”选择实际连接游戏的配置，例如 `oas1`。
3. 点击“连接模拟器”。
4. 确认预览画面就是体验服，并且当前停在挑战按钮可见的页面。
5. 点击“截取当前帧到图片列表”。
6. 在图片列表中确认截图分辨率仍为 `1280x720`。

也可以选择“本地图片”：先使用模拟器截一张原始截图，再上传到 OAS Web。不要使用聊天软件转发后的压缩图。

### B. 选择唯一规则

右侧文件树选择：

```text
/ -> ExperienceClimb -> as -> image.json
```

规则列表中只应看到：

```text
act_fire
```

不要再选择 `pages.json`、`ocr.json`、`click.json` 或其他活动规则；当前实现已经不使用这些规则。

### C. 标注 `act_fire`

1. 选中规则 `act_fire`。
2. 选中刚才截取的、挑战按钮完整可见的截图。
3. 在画布上框选挑战按钮本身或按钮中稳定的图标/文字，作为 `roiFront`。
4. `roiFront` 不要包含大面积背景、动态角色或数字；框太大容易受动画影响。
5. 框选挑战按钮可能出现的搜索范围，作为 `roiBack`。如果按钮位置固定，`roiBack` 可以比 `roiFront` 大一圈；不要把整个画面都作为搜索范围。
6. 保持以下关键字段：

   ```text
   itemName: act_fire
   imageName: as_act_fire.png
   method: Template matching
   threshold: 0.8
   ```

7. 点击“裁剪/保存图片”，生成新的 `as_act_fire.png`。
8. 最好再截取一张同页面截图，使用“测试”确认两张截图都能识别。
9. 点击“保存规则”。

`roiFront` 是模板小图，`roiBack` 是搜索范围，格式均为 `x,y,w,h`。图片规则的点击位置取自匹配到的模板位置，因此 `roiFront` 必须覆盖实际可点击的按钮区域。

### D. 保存后检查生成结果

保存成功后检查：

```text
tasks/ExperienceClimb/as/image.json
tasks/ExperienceClimb/as/as_act_fire.png
tasks/ExperienceClimb/assets.py
```

`assets.py` 中应该只需要看到类似内容：

```python
I_ACT_FIRE = RuleImage(... file="./tasks/ExperienceClimb/as/as_act_fire.png")
```

如果 OAS Web 提示生成成功但 `assets.py` 中出现大量旧规则，说明旧 JSON 仍被扫描；当前目录应只保留 `image.json` 这一份规则 JSON。不要把生成结果保存到 `tasks/ActivityShikigami/`。

## 四、配置和运行

### 1. 体验服任务配置

在 GUI 的“限时活动”中选择“体验服爬塔”。本任务只读取以下配置：

```text
experience_climb.general_climb.ap_limit
experience_climb.general_climb.limit_time
experience_climb.ap_battle_conf
```

建议第一次测试：

```text
ap_limit = 1
limit_time = 00:10:00
```

`ap_battle_conf` 使用通用战斗配置，按正式爬塔已经验证过的队伍、预设、绿标和战斗超时设置即可。体验服任务不会替你切换御魂或锁定阵容，所以启动前应手动把阵容调整好。

### 2. 启动前检查

1. 模拟器停在体验服体力爬塔页面。
2. 挑战按钮完整可见。
3. 挑战按钮模板来自体验服的新截图。
4. `ap_limit` 先设为 `1`。
5. `ap_battle_conf` 已配置通用战斗。
6. 正式服任务仍使用 `ActivityShikigami`，不要把体验服图片覆盖到正式服目录。

### 3. 预期日志和流程

正常情况下日志会出现：

```text
Experience climb start
Experience climb challenge clicked
General battle start
Current count: 1
Experience climb count limit reached
```

战斗结束并再次看到挑战按钮后，任务才会进入下一轮。达到 `ap_limit` 或 `limit_time` 后，任务结束并交回调度器。

## 五、问题排查

### 1. 一直不点击

优先检查：

- 游戏分辨率是否仍是 `1280x720`。
- 当前是否真的在挑战按钮可见的页面。
- 新模板是否只截取了按钮，而不是整张截图。
- `roiBack` 是否覆盖按钮实际位置。
- 阈值是否过高；可先从 `0.8` 小幅调整到 `0.75`，不要直接设得很低。

### 2. 点击后没有进入战斗

这通常不是 `act_fire` 图片问题，而是点击后游戏页面或通用战斗配置的问题。先观察按钮是否发生了按下反馈，再检查：

- `ap_battle_conf` 是否配置正确。
- 通用战斗公共页面资源是否能够识别准备页和战斗页。
- 是否有弹窗遮挡了进入战斗的过程。

### 3. 战斗结束后不继续

任务用同一张 `act_fire` 作为战斗结束后的回到活动页判断。重新截取一张战斗结束后、挑战按钮重新出现的截图，确认按钮外观没有因为次数、状态或动画发生变化。如果结束后的按钮样式确实不同，才需要再讨论增加第二张图片；当前代码没有为第二张图片预留流程。

### 4. 启动时报旧模块找不到

确认 `tasks/ExperienceClimb/script_task.py` 只导入：

```python
from tasks.ExperienceClimb.base_act import ExperienceClimbAct
```

当前不应再导入 `activities` 或 `page.py`。

## 六、停止本地服务

标注完成后，在运行 `server.py` 的终端按 `Ctrl+C` 停止 OAS Web。任务测试结束后，按需手动关闭模拟器。
