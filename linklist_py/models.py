# linklist_py/models.py
from django.db import models
import uuid
try:
    # Django 3.1+ 提供 JSONField
    from django.db.models import JSONField
except Exception:
    JSONField = None

class LinkedListRecord(models.Model):
    """
    用于保存单链表的快照/教学记录。
    - id: UUID primary key
    - name: 可读名字
    - data: 节点数组（JSON）
    - created_at, updated_at: 时间戳
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, blank=True)
    if JSONField:
        data = JSONField(default=list)  # 存储当前节点列表，例如 [1,2,3]
    else:
        data = models.TextField(blank=True, default='[]')  # 如果没有 JSONField，请保存为 JSON 文本
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"LinkedListRecord {self.name or str(self.id)}"
