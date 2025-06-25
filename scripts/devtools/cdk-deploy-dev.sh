#!/usr/bin/env bash
cd cdk
npx cdk deploy --require-approval never --all -c envName=dev