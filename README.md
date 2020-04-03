# YAML vizualizer
Quick and dirty script that allows to bring vizual representation
of yaml content.

## Prerequisites
- Install grpahviz software https://www.graphviz.org/
- Install python requirements in your run time environment

## Method of execution
** python yml2pdf.py <yamlfile> <pdfile>

### Example 
Sample yaml content ( AWS Policy )
```
---
Version: '2012-10-17'
Statement:
- Sid: ListAllS3Buckets
  Effect: Allow
  Action:
  - s3:ListAllMyBuckets
  Resource: arn:aws:s3:::*
- Sid: AllowBucketLevelActions
  Effect: Allow
  Action:
  - s3:ListBucket
  - s3:GetBucketLocation
  Resource: arn:aws:s3:::*
- Sid: AllowBucketObjectActions
  Effect: Allow
  Action:
  - s3:PutObject
  - s3:PutObjectAcl
  - s3:GetObject
  - s3:GetObjectAcl
  - s3:DeleteObject
  Resource: arn:aws:s3:::*/*
- Sid: RequireMFAForProductionBucket
  Effect: Deny
  Action: s3:*
  Resource:
  - arn:aws:s3:::Production/*
  - arn:aws:s3:::Production
  Condition:
    NumericGreaterThanIfExists:
      aws:MultiFactorAuthAge: '1800'
```

Produced PDF representation
![sample.png](sample.png?raw=true "PDF")
