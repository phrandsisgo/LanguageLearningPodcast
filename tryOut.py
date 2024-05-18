import re

story ="""Mal schauen ob dies funktioniert! Lisa préparait depuis des semaines sa soirée avec ses amis! Elle avait invité ses amis les plus proches et avait prévu un menu délicieux. Elle voulait que cette soirée soit inoubliable.

Le jour de la soirée, Lisa était très excitée? Elle avait tout préparé avec soin. Elle avait décoré son appartement avec des guirlandes lumineuses et avait mis de la musique d'ambiance.

Les invités sont arrivés à l'heure prévue. Ils étaient tous très accueillants et ont complimenté Lisa pour sa décoration? Ils ont aussi beaucoup goûté le menu qu'elle avait préparé!

La soirée s'est déroulée à merveille. Les amis de Lisa ont beaucoup discuté et ri. Ils ont aussi dansé et chanté. Lisa était très heureuse de voir ses amis s'amuser autant.

À la fin de la soirée, les invités sont partis très satisfaits. Ils ont remercié Lisa pour son hospitalité et lui ont dit que c'était une soirée inoubliable.

Lisa était très contente de la réussite de sa soirée. Elle avait passé un excellent moment avec ses amis et avait créé des souvenirs qui resteront gravés dans sa mémoire."""

arrayForEachSentence = re.split('[.!?]', story)
for sentence in arrayForEachSentence:
    print("\033[92m" + sentence + "\033[0m")
    print("\n")
    print("next sentence:")