with open('./Outputs/resultats.csv', 'w') as filout:
	with open('./Outputs/Noms.txt', 'r') as filin:
		for ligne in filin:
			ligne = ligne[:-1]
			with open('./Outputs/foldx_analysis/{}'.format(ligne), 'r') as donne:
				for res in donne:
					res = res.split()[1]
					filout.write(res + '\n')