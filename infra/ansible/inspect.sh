#!/bin/bash
# =============================================================================
# Verification wrapper for verify.yml — runs tests and writes log + JUnit XML
#
# Usage:
#   ./inspect.sh                    # All modules
#   ./inspect.sh module01           # Module 01 only
#   ./inspect.sh module02           # Module 02 only
#
# Output: reports/YYYY-MM-DD_HH-MM_inspection.log
#         reports/YYYY-MM-DD_HH-MM_inspection.xml (JUnit)
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M)
LOG_FILE="reports/${TIMESTAMP}_inspection.log"
XML_PREFIX="reports/${TIMESTAMP}_inspection"

mkdir -p reports

TAGS=""
if [ -n "$1" ]; then
    TAGS="--tags $1"
fi

echo "=== INSPECTION $(date) ===" | tee "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

JUNIT_OUTPUT_DIR=reports \
JUNIT_TASK_RELATIVE_PATH=true \
ansible-playbook -i inventory.local.yml verify.yml $TAGS 2>&1 | \
    grep -E '(^PLAY|^TASK|ok:|fatal:|changed:|PLAY RECAP|"msg":)' | \
    sed 's/\x1b\[[0-9;]*m//g' | \
    tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "=== INSPECTION COMPLETE $(date) ===" | tee -a "$LOG_FILE"
echo ""
echo "Log: $LOG_FILE"

LATEST_XML=$(ls -t reports/*.xml 2>/dev/null | head -1)
if [ -n "$LATEST_XML" ]; then
    mv "$LATEST_XML" "${XML_PREFIX}.xml"
    echo "JUnit XML: ${XML_PREFIX}.xml"
fi
