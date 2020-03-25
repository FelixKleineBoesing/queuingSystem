cd ./tests
test_output="$(coverage run -m --source="../src" pytest)"
tail_output=$(echo "$test_output" | tail -n -1)
coverage report -m
cd ../

if [[ "$tail_output" =~ failed ]] || [[ "$tail_output" =~ error ]]; then
    echo "At least one test failed"
    exit 1
fi

echo "All tests were passed"
