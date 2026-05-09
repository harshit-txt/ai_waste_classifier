import tensorflow as tf
from preprocess import train_data, val_data, test_data, NUM_CLASSES

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    'saved_model/best_model.h5',
    monitor='val_accuracy',    
    save_best_only=True,       
    verbose=1                  
)

early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=5,        
    verbose=1,
    restore_best_weights=True   
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_accuracy',
    factor=0.2,        
    patience=3,        
    verbose=1
)

print("\n Starting Phase 1 Training — base model frozen \n")

import os
os.makedirs('saved_model', exist_ok=True)

history = model.fit(
    train_data,               
    epochs=1,                
    validation_data=val_data, 
    callbacks=[checkpoint, early_stop, reduce_lr]
)


print("\n Starting Phase 2 — Fine tuning last 30 layers \n")
base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_fine = model.fit(
    train_data,
    epochs=1,
    validation_data=val_data,
    callbacks=[checkpoint, early_stop, reduce_lr]
)

print("\n Evaluating on test set \n")
test_loss, test_accuracy = model.evaluate(test_data)

print(f"\n Final Test Accuracy: {test_accuracy * 100:.2f}%")
model.save('saved_model/waste_classifier.keras')

print("\n Model saved to saved_model/waste_classifier")