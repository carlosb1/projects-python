#!/bin/bash
pushd ./
cd src
pytest -sv tests/*py && pytest --cov=./ tests/*py
popd
