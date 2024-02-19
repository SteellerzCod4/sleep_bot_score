# Sleep Bot Score
Данный бот выводит числовую характеристику сна, на
основе времени засыпания, пробуждения и длительности сна. 
Доступ к статистике вашего режима сна позволяет отслеживать прогресс исправления распорядка сна.

# Использование
Перед сном нажмите кнопку "Время засыпания", так бот зарегестрирует время когда вы легли. 
Если же вы хотите изменить данное время, нажмите кнопку "Редактировать" или нажмите кнопку "Время засыпания" повторно.

Когда вы проснулись нажмите кнопку "Время пробуждения", так бот зафиксирует время пробуждение и окончательно высчитает качество вашего режима сна, занеся всю информацию в статистику.

Если вы хотите узнать статистику нажмите кнопку "Статистика"

Если хотите исправить ранее введенное время сна или изменить часы засыпания и пробуждения, то нажмите кнопку "Редактирование"

# Метрика сна
Бот агрегирует 3 метрики (Retire Score, WakeUp Score и Duration Score) в одну финальную метрику F1-Sleep Score

## Retire Score
Retire Score представляет из себя R2 Score по расчету качества вашего засыпания и расчитывается как:
1 - ("время засыпания" - "оптимальное время засыпания") / ("крайнее время засыпания" - "оптимальное время засыпания")

Таким образом, Retire Score фиксирует насколько сильно ваше время засыпания отличается от самого плохо времени засыпания, когда вы ложитесь в крайний срок.
Чем меньшую долю составляет ваше пробуждение от худшего сценария, тем меньшее число вычитается из единицы, которая означает наилучшее время засыпания.

## WakeUP Score
WakeUP Score это также R2 Score-подобная метрика, которая работает по тому же принципу, что и Retire Score, но которая фиксирует насколько ваше пробуждение отличается от самого плохо сценария пробуждения. 
Данная метрика рассчитывется по формуле: 
1 - ("время пробуждения" - "оптимальное время пробуждения") / ("крайнее время пробуждения" - "оптимальное время пробуждения")

## Duration Score
Duration Score отличается от метрик Retire Score и WakeUP score, стремясь оценить качество продолжительности сна, ведь даже если вы ложитесь и встаете вовремя, это еще не значит, что данного времени сна достаточно для вашего организма.
Формула:
1 / (exp(("получившаяся продолжительность сна" - "оптимальная продолжительность сна")**2) / 4)
Причины выбора именно такой формулы вызвано тем, что она должна быть в диапазоне от [0, 1], 
быть симметрично убывающей возле точки оптимальной продолжительности сна и убывать экспоненциально, 
сильно штрафую как за недосып, так и за пересыпание, которое склонно накапливаться в организме и негативно на него влиять.
Примечание: Duration Score на самом деле имеет диапазон значений (0, 1], то есть не достигает нуля, но програмно это исправлено доопределением функции в нуле.

# Sleep Bot Score

This bot provides a numerical representation of sleep quality based on bedtime, wake-up time, and sleep duration. Access to your sleep schedule statistics allows tracking progress in improving sleep patterns.

## Usage

Before sleep, press the "Bedtime" button to register the time you went to bed. If you wish to change this time, press the "Edit" button or press the "Bedtime" button again.

When you wake up, press the "Wake-up Time" button to record the wake-up time, and the bot will calculate the quality of your sleep, adding all the information to the statistics.

If you want to view the statistics, press the "Statistics" button.

If you need to correct previously entered sleep times or change the bedtime and wake-up hours, press the "Edit" button.

## Sleep Metrics

The bot aggregates 3 metrics (Retire Score, WakeUp Score, and Duration Score) into one final metric, F1-Sleep Score.

### Retire Score

Retire Score represents the R2 Score for calculating the quality of your bedtime and is calculated as:

$$ 1 - \frac{{\text{"bedtime"} - \text{"optimal bedtime"}}}{{\text{"latest bedtime"} - \text{"optimal bedtime"}}} $$

Retire Score indicates how much your bedtime deviates from the worst bedtime scenario when you go to bed at the latest possible time. The closer your bedtime is to the worst-case scenario, the smaller the fraction subtracted from one, indicating the best bedtime.

### WakeUP Score

WakeUP Score is also an R2 Score-like metric working on the same principle as Retire Score but measuring how your wake-up time differs from the worst wake-up scenario. This metric is calculated as:

$$ 1 - \frac{{\text{"wake-up time"} - \text{"optimal wake-up time"}}}{{\text{"latest wake-up time"} - \text{"optimal wake-up time"}}} $$

### Duration Score

Duration Score differs from Retire Score and WakeUP Score, aiming to evaluate the quality of sleep duration. Even if you go to bed and wake up on time, it doesn't necessarily mean that the duration of sleep is sufficient for your body. The formula is:

$$ \frac{1}{{\exp\left(\left(\text{"actual sleep duration"} - \text{"optimal sleep duration"}\right)^2\right) / 4}} $$

The choice of this formula is motivated by the need for it to be in the range [0, 1], symmetrically decreasing around the optimal sleep duration point, and exponentially decreasing, penalizing both undersleeping and oversleeping, which tend to accumulate in the body and have negative effects.

*Note:* Duration Score actually has a range of values (0, 1], meaning it does not reach zero, but this is programmatically adjusted by defining the function at zero.

### Final Score: F1-Sleep Score

F1-Sleep Score is the harmonic mean of all three previous metrics and is an F1-Score-like metric, which by its nature tends to shift the final evaluation towards the aggregated metric with the lowest value. This is done to emphasize that healthy sleep is only possible if all three metrics have good values, and success in any of them does not override failure in any other metric. The final calculation formula is:

$$ \frac{{3 \times \text{Retire Score} \times \text{WakeUP Score} \times \text{Duration Score}}}{{\text{Retire Score} + \text{WakeUP Score} + \text{Duration Score}}} $$
