import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

export_file_url = 'https://www.dropbox.com/s/tau05qtkbqsngyq/export.pkl?dl=1'
export_file_name = 'export.pkl'

classes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,'hyundai_getz']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    clases_car = ['AM General Hummer SUV 2000','Acura RL Sedan 2012','Acura TL Sedan 2012','Acura TL Type-S 2008','Acura TSX Sedan 2012','Acura Integra Type R 2001','Acura ZDX Hatchback 2012','Aston Martin V8 Vantage Convertible 2012','Aston Martin V8 Vantage Coupe 2012','Aston Martin Virage Convertible 2012','Aston Martin Virage Coupe 2012','Audi RS 4 Convertible 2008','Audi A5 Coupe 2012','Audi TTS Coupe 2012','Audi R8 Coupe 2012','Audi V8 Sedan 1994','Audi 100 Sedan 1994','Audi 100 Wagon 1994','Audi TT Hatchback 2011','Audi S6 Sedan 2011','Audi S5 Convertible 2012','Audi S5 Coupe 2012','Audi S4 Sedan 2012','Audi S4 Sedan 2007','Audi TT RS Coupe 2012','BMW ActiveHybrid 5 Sedan 2012','BMW 1 Series Convertible 2012','BMW 1 Series Coupe 2012','BMW 3 Series Sedan 2012','BMW 3 Series Wagon 2012','BMW 6 Series Convertible 2007','BMW X5 SUV 2007','BMW X6 SUV 2012','BMW M3 Coupe 2012','BMW M5 Sedan 2010','BMW M6 Convertible 2010','BMW X3 SUV 2012','BMW Z4 Convertible 2012','Bentley Continental Supersports Conv. Convertible 2012','Bentley Arnage Sedan 2009','Bentley Mulsanne Sedan 2011','Bentley Continental GT Coupe 2012','Bentley Continental GT Coupe 2007','Bentley Continental Flying Spur Sedan 2007','Bugatti Veyron 16.4 Convertible 2009','Bugatti Veyron 16.4 Coupe 2009','Buick Regal GS 2012','Buick Rainier SUV 2007','Buick Verano Sedan 2012','Buick Enclave SUV 2012','Cadillac CTS-V Sedan 2012','Cadillac SRX SUV 2012','Cadillac Escalade EXT Crew Cab 2007','Chevrolet Silverado 1500 Hybrid Crew Cab 2012','Chevrolet Corvette Convertible 2012','Chevrolet Corvette ZR1 2012','Chevrolet Corvette Ron Fellows Edition Z06 2007','Chevrolet Traverse SUV 2012','Chevrolet Camaro Convertible 2012','Chevrolet HHR SS 2010','Chevrolet Impala Sedan 2007','Chevrolet Tahoe Hybrid SUV 2012','Chevrolet Sonic Sedan 2012','Chevrolet Express Cargo Van 2007','Chevrolet Avalanche Crew Cab 2012','Chevrolet Cobalt SS 2010','Chevrolet Malibu Hybrid Sedan 2010','Chevrolet TrailBlazer SS 2009','Chevrolet Silverado 2500HD Regular Cab 2012','Chevrolet Silverado 1500 Classic Extended Cab 2007','Chevrolet Express Van 2007','Chevrolet Monte Carlo Coupe 2007','Chevrolet Malibu Sedan 2007','Chevrolet Silverado 1500 Extended Cab 2012','Chevrolet Silverado 1500 Regular Cab 2012','Chrysler Aspen SUV 2009','Chrysler Sebring Convertible 2010','Chrysler Town and Country Minivan 2012','Chrysler 300 SRT-8 2010','Chrysler Crossfire Convertible 2008','Chrysler PT Cruiser Convertible 2008','Daewoo Nubira Wagon 2002','Dodge Caliber Wagon 2012','Dodge Caliber Wagon 2007','Dodge Caravan Minivan 1997','Dodge Ram Pickup 3500 Crew Cab 2010','Dodge Ram Pickup 3500 Quad Cab 2009','Dodge Sprinter Cargo Van 2009','Dodge Journey SUV 2012','Dodge Dakota Crew Cab 2010','Dodge Dakota Club Cab 2007','Dodge Magnum Wagon 2008','Dodge Challenger SRT8 2011','Dodge Durango SUV 2012','Dodge Durango SUV 2007','Dodge Charger Sedan 2012','Dodge Charger SRT-8 2009','Eagle Talon Hatchback 1998','FIAT 500 Abarth 2012','FIAT 500 Convertible 2012','Ferrari FF Coupe 2012','Ferrari California Convertible 2012','Ferrari 458 Italia Convertible 2012','Ferrari 458 Italia Coupe 2012','Fisker Karma Sedan 2012','Ford F-450 Super Duty Crew Cab 2012','Ford Mustang Convertible 2007','Ford Freestar Minivan 2007','Ford Expedition EL SUV 2009','Ford Edge SUV 2012','Ford Ranger SuperCab 2011','Ford GT Coupe 2006','Ford F-150 Regular Cab 2012','Ford F-150 Regular Cab 2007','Ford Focus Sedan 2007','Ford E-Series Wagon Van 2012','Ford Fiesta Sedan 2012','GMC Terrain SUV 2012','GMC Savana Van 2012','GMC Yukon Hybrid SUV 2012','GMC Acadia SUV 2012','GMC Canyon Extended Cab 2012','Geo Metro Convertible 1993','HUMMER H3T Crew Cab 2010','HUMMER H2 SUT Crew Cab 2009','Honda Odyssey Minivan 2012','Honda Odyssey Minivan 2007','Honda Accord Coupe 2012','Honda Accord Sedan 2012','Hyundai Veloster Hatchback 2012','Hyundai Santa Fe SUV 2012','Hyundai Tucson SUV 2012','Hyundai Veracruz SUV 2012','Hyundai Sonata Hybrid Sedan 2012','Hyundai Elantra Sedan 2007','Hyundai Accent Sedan 2012','Hyundai Genesis Sedan 2012','Hyundai Sonata Sedan 2012','Hyundai Elantra Touring Hatchback 2012','Hyundai Azera Sedan 2012','Infiniti G Coupe IPL 2012','Infiniti QX56 SUV 2011','Isuzu Ascender SUV 2008','Jaguar XK XKR 2012','Jeep Patriot SUV 2012','Jeep Wrangler SUV 2012','Jeep Liberty SUV 2012','Jeep Grand Cherokee SUV 2012','Jeep Compass SUV 2012','Lamborghini Reventon Coupe 2008','Lamborghini Aventador Coupe 2012','Lamborghini Gallardo LP 570-4 Superleggera 2012','Lamborghini Diablo Coupe 2001','Land Rover Range Rover SUV 2012','Land Rover LR2 SUV 2012','Lincoln Town Car Sedan 2011','MINI Cooper Roadster Convertible 2012','Maybach Landaulet Convertible 2012','Mazda Tribute SUV 2011','McLaren MP4-12C Coupe 2012','Mercedes-Benz 300-Class Convertible 1993','Mercedes-Benz C-Class Sedan 2012','Mercedes-Benz SL-Class Coupe 2009','Mercedes-Benz E-Class Sedan 2012','Mercedes-Benz S-Class Sedan 2012','Mercedes-Benz Sprinter Van 2012','Mitsubishi Lancer Sedan 2012','Nissan Leaf Hatchback 2012','Nissan NV Passenger Van 2012','Nissan Juke Hatchback 2012','Nissan 240SX Coupe 1998','Plymouth Neon Coupe 1999','Porsche Panamera Sedan 2012','Ram C/V Cargo Van Minivan 2012','Rolls-Royce Phantom Drophead Coupe Convertible 2012','Rolls-Royce Ghost Sedan 2012','Rolls-Royce Phantom Sedan 2012','Scion xD Hatchback 2012','Spyker C8 Convertible 2009','Spyker C8 Coupe 2009','Suzuki Aerio Sedan 2007','Suzuki Kizashi Sedan 2012','Suzuki SX4 Hatchback 2012','Suzuki SX4 Sedan 2012','Tesla Model S Sedan 2012','Toyota Sequoia SUV 2012','Toyota Camry Sedan 2012','Toyota Corolla Sedan 2012','Toyota 4Runner SUV 2012','Volkswagen Golf Hatchback 2012','Volkswagen Golf Hatchback 1991','Volkswagen Beetle Hatchback 2012','Volvo C30 Hatchback 2012','Volvo 240 Sedan 1993','Volvo XC90 SUV 2007','smart fortwo Convertible 2012','Hyundai getz 2006'];
    return JSONResponse({'result': str(clases_car[int(prediction)])})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
