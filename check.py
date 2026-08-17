import modal, deploy
@deploy.app.function(image=deploy.llama_image)
def check():
    import os
    print('Contents of /model:')
    os.system('ls -la /model')
    os.system('find /model')
