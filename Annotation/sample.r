 nsample <- 300


data<- read.csv("C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Annotation/a.csv")
# sample data

ndata <- nrow(data)
print(ndata)
samp_idx <- sample(seq_len(nrow(data)), nsample)
new_data <- data[samp_idx, ]
new_data


write.csv(new_data,"C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Annotation/new.csv", row.names = FALSE)