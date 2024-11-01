# Generated by Django 4.2.7 on 2024-10-29 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MetricObject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="创建者")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="更新者")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="修改时间")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="指标对象名称")),
                ("type", models.CharField(max_length=50, verbose_name="指标对象类型")),
            ],
            options={
                "verbose_name": "指标对象",
                "verbose_name_plural": "指标对象",
            },
        ),
        migrations.CreateModel(
            name="MetricGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="创建者")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="更新者")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="修改时间")),
                ("name", models.CharField(max_length=100, verbose_name="指标分组名称")),
                ("description", models.TextField(blank=True, null=True, verbose_name="指标分组描述")),
                (
                    "metric_object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="monitor.metricobject", verbose_name="指标对象"
                    ),
                ),
            ],
            options={
                "verbose_name": "指标分组",
                "verbose_name_plural": "指标分组",
            },
        ),
        migrations.CreateModel(
            name="Metric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="创建者")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="更新者")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="修改时间")),
                ("name", models.CharField(max_length=100, verbose_name="指标名称")),
                ("type", models.CharField(max_length=50, verbose_name="指标类型")),
                ("description", models.TextField(blank=True, null=True, verbose_name="指标描述")),
                ("dimensions", models.JSONField(default=list, verbose_name="维度")),
                (
                    "metric_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="monitor.metricgroup", verbose_name="指标分组"
                    ),
                ),
                (
                    "metric_object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="monitor.metricobject", verbose_name="指标对象"
                    ),
                ),
            ],
            options={
                "verbose_name": "指标",
                "verbose_name_plural": "指标",
                "unique_together": {("metric_object", "name")},
            },
        ),
    ]