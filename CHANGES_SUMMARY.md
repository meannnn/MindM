# Activity Intent 重构总结

## 修改概述

根据用户需求，将 `activity_intent` 从全局字段改为 `learning_activities` 中每个活动项的独立字段，实现了每个学习活动都有自己的活动意图，并在表格中对应的每一行输出。

## 具体修改内容

### 1. 数据结构修改 (`schemas/teaching_design_schema.py`)

#### ActivityInfo 类
- **新增字段**: `activity_intent: str` - 活动意图
- **修改前**: 只有 `name`, `teacher_activity`, `student_activity`
- **修改后**: 包含 `name`, `teacher_activity`, `student_activity`, `activity_intent`

#### TeachingDesignData 类
- **移除字段**: `activity_intent: str` - 全局活动意图字段
- **保留**: `learning_activities: List[ActivityInfo]` - 学习活动列表

#### JSON Schema 更新
- **learning_activities 数组元素结构**:
  - 新增: `"activity_intent": {"type": "string", "description": "活动意图"}`
  - 必需字段: `["name", "teacher_activity", "student_activity", "activity_intent"]`
- **移除全局字段**: `"activity_intent"` 从根级别移除
- **必需字段列表**: 移除 `"activity_intent"`

#### 示例数据更新
- 为每个学习活动添加独立的 `activity_intent` 字段
- 移除全局的 `activity_intent` 字段

#### 数据验证逻辑
- 更新验证逻辑，确保每个学习活动都包含 `activity_intent` 字段

### 2. LLM 提示词修改 (`prompts/teaching_design_prompt.py`)

#### JSON 模板更新
- **learning_activities 数组元素**:
  - 新增: `"activity_intent": "该活动的教学意图和目的"`
- **移除**: 全局的 `"activity_intent"` 字段

#### 内容生成指南
- 强调每个学习活动都必须包含独立的 `activity_intent` 字段
- 说明该环节的具体教学意图和目的

#### JSON Schema 说明
- 更新 `learning_activities` 数组元素结构说明
- 从必需字段列表中移除全局 `activity_intent`

### 3. 模板处理器修改 (`docx_processor/template_processor.py`)

#### 数据转换逻辑
- **移除**: 从模板数据中移除全局 `activity_intent` 字段
- **更新**: 使用每个活动自己的 `activity.intent` 而不是全局的 `design_data.activity_intent`

#### 学习活动处理
- 每个活动现在使用自己的 `activity_intent` 字段
- 确保在 Word 模板中每个活动行都包含对应的活动意图

#### 测试数据更新
- 更新测试数据以匹配新的数据结构

## 影响范围

### 正面影响
1. **更精确的活动意图**: 每个学习活动都有自己特定的教学意图
2. **更好的表格显示**: 在 Word 模板中，每个活动行都包含对应的活动意图
3. **更清晰的数据结构**: 避免了全局活动意图与具体活动不匹配的问题
4. **更灵活的模板设计**: 支持每个活动独立的活动意图展示

### 兼容性考虑
- **向后兼容**: 旧的数据格式将无法通过新的验证
- **模板更新**: Word 模板需要相应更新以支持新的数据结构
- **LLM 输出**: LLM 现在需要为每个活动生成独立的意图

## 验证结果

通过测试验证，所有修改都已正确实施：
- ✅ 数据结构创建成功
- ✅ 学习活动包含独立的 activity_intent
- ✅ 数据验证通过
- ✅ JSON 输出格式正确

## 使用示例

新的 JSON 格式示例：
```json
{
  "learning_activities": [
    {
      "name": "导入环节",
      "teacher_activity": "播放春天相关的音乐，引导学生回忆春天的景象",
      "student_activity": "听音乐，回忆并分享春天的印象",
      "activity_intent": "通过音乐导入激发学生学习兴趣，营造春天的氛围"
    },
    {
      "name": "整体感知",
      "teacher_activity": "指导学生朗读课文，整体把握文章内容",
      "student_activity": "朗读课文，概括文章主要内容",
      "activity_intent": "通过朗读整体感知文章内容，培养学生语感和理解能力"
    }
  ]
}
```

## 注意事项

1. **Word 模板更新**: 需要确保 Word 模板支持新的数据结构
2. **LLM 训练**: 确保 LLM 能够为每个活动生成合适的意图描述
3. **数据迁移**: 如果有旧数据，需要进行相应的数据迁移
4. **测试覆盖**: 建议对所有相关功能进行全面测试
