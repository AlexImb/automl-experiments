# H2O.ai + Kafka

```
cat ./datasets/airlines-allyears2k.csv | kafkacat -P -b localhost -t airlines_stream
```

```
echo "1987,10,19,1,749,730,922,849,PS,1451,NA,93,79,NA,33,19,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA,YES,YES" | kafkacat -P -b localhost -t airlines_prediction_input
```

```
kafkacat -b localhost -t airlines_prediction_output
```
