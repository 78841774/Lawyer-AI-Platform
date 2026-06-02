# File Storage Blueprint

File Storage Blueprint 定义 Lawyer AI Platform 的文件存储方案。

文件存储负责保存案件原始材料、OCR 结果、解析结果、AI 分析结果、报告文件和历史版本。结构化业务数据保存在数据库中，文件内容通过 storage_path、ocr_path、output_ref 等字段关联。

## 存储对象

### 原始材料

保存用户上传的合同、凭证、聊天记录、函件、裁判文书、证据目录等原始文件。

要求：

* 保留原始文件名和上传时间。
* 生成稳定 material_id。
* 不直接覆盖原始文件。
* 支持按 case_id 隔离。

### OCR 结果

保存 OCR 文本、页码、段落、坐标和置信度。

要求：

* OCR 结果应与 material_id 关联。
* 支持 JSON、TXT 或结构化分片格式。
* 支持事实来源定位到页码、段落或文本片段。

### 分析结果

保存事实抽取、法律分析、策略生成等 AI 运行结果。

要求：

* 结果文件应包含 job_id、request_id、schema_version。
* 结构化主数据写入数据库。
* 大体量上下文、原始模型输出和中间过程可写入文件存储。

### 报告文件

保存法律分析报告、诉讼策略报告、证据清单、起诉状草稿、答辩状草稿等输出文件。

要求：

* 支持 Markdown、DOCX、PDF 等格式。
* 支持 report_id 和 version。
* 支持导出、归档和历史版本追溯。

## 路径规范

建议路径：

```text
cases/
  {case_id}/
    materials/
      originals/
        {material_id}/{filename}
      ocr/
        {material_id}/ocr.json
      parsed/
        {material_id}/chunks.json
    ai-results/
      facts/
        {job_id}/result.json
      legal/
        {job_id}/result.json
      strategy/
        {job_id}/result.json
    reports/
      {report_id}/
        v{version}/
          report.md
          report.docx
          report.pdf
    audit/
      {request_id}.json
```

## 版本管理

* 原始材料不覆盖，新增文件生成新的 material_id 或 file_version。
* OCR 和解析结果按 material_id 记录版本。
* 分析结果按 job_id 和 request_id 记录。
* 报告按 report_id 和 version 记录。
* Experience Package 切换后生成的新结果应记录 package_id 和 package_version。

## 存储实现建议

本地开发可使用本地目录或 MinIO。

测试环境和生产环境建议使用对象存储，例如 S3、OSS 或兼容 S3 的存储服务。

数据库只保存文件元数据和路径引用，不保存大文件二进制内容。

## 安全要求

* 文件访问应按 case_id 和用户权限控制。
* 下载链接应使用短期有效签名。
* 删除操作应保留审计日志。
* 生产环境应启用存储加密和备份策略。
