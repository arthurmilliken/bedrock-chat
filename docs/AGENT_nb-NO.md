# LLM-drevet Agent (ReAct)

## Hva er Agenten (ReAct)?

En Agent er et avansert AI-system som benytter store språkmodeller (LLM-er) som sin sentrale beregningsmotorenhet. Den kombinerer resonnementsfunksjonene til LLM-er med tilleggsfunksjonaliteter som planlegging og verktøysbruk for å autonomt utføre komplekse oppgaver. Agenter kan dele ned kompliserte forespørsler, generere trinnvise løsninger og samhandle med eksterne verktøy eller API-er for å innhente informasjon eller utføre deloppgaver.

Denne eksempelet implementerer en Agent ved bruk av [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) tilnærmingen. ReAct gjør det mulig for agenten å løse komplekse oppgaver ved å kombinere resonnement og handlinger i en iterativ tilbakemeldingssløyfe. Agenten går gjentatte ganger gjennom tre nøkkeltrinn: Tanke, Handling og Observasjon. Den analyserer den nåværende situasjonen ved bruk av LLM-en, bestemmer neste handling som skal utføres, gjennomfører handlingen ved bruk av tilgjengelige verktøy eller API-er, og lærer av de observerte resultatene. Denne kontinuerlige prosessen gjør at agenten kan tilpasse seg dynamiske omgivelser, forbedre nøyaktigheten i oppgaveløsning og levere kontekstbevisste løsninger.

## Eksempel på brukstilfelle

En Agent som bruker ReAct kan benyttes i ulike scenarioer og gir nøyaktige og effektive løsninger.

### Tekst-til-SQL

En bruker ber om "de totale salgstallene for forrige kvartal." Agenten tolker denne forespørselen, konverterer den til en SQL-spørring, kjører den mot databasen og presenterer resultatene.

### Finansiell prognose

En finansanalytiker trenger å lage en prognose for neste kvartals inntekter. Agenten samler inn relevante data, utfører nødvendige beregninger ved hjelp av finansielle modeller og genererer en detaljert prognose, som sikrer nøyaktigheten i fremskrivningene.

## Slik bruker du Agent-funksjonen

For å aktivere Agent-funksjonaliteten for din tilpassede chatbot, følg disse trinnene:

Det finnes to måter å bruke Agent-funksjonen på:

### Bruk av verktøybruk

For å aktivere Agent-funksjonaliteten med verktøybruk for din tilpassede chatbot, følg disse trinnene:

1. Naviger til Agent-seksjonen i den tilpassede bot-skjermen.

2. I Agent-seksjonen vil du finne en liste over tilgjengelige verktøy som kan brukes av Agenten. Som standard er alle verktøy deaktivert.

3. For å aktivere et verktøy, slår du ganske enkelt på bryteren ved siden av det ønskede verktøyet. Når et verktøy er aktivert, vil Agenten ha tilgang til det og kan bruke det ved behandling av brukerforespørsler.

![](./imgs/agent_tools.png)

4. For eksempel kan verktøyet "Internett-søk" la Agenten hente informasjon fra internett for å svare på brukerens spørsmål.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Du kan utvikle og legge til dine egne tilpassede verktøy for å utvide Agent-funksjonaliteten. Se [Hvordan utvikle dine egne verktøy](#how-to-develop-your-own-tools)-seksjonen for mer informasjon om å opprette og integrere tilpassede verktøy.

### Bruk av Bedrock Agent

Du kan bruke en [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) opprettet i Amazon Bedrock.

Opprett først en Agent i Bedrock (f.eks. via Management Console). Deretter angir du Agent-ID-en i innstillingsskjermen for den tilpassede boten. Når dette er gjort, vil din chatbot utnytte Bedrock Agent for å behandle brukerforespørsler.

![](./imgs/bedrock_agent_tool.png)

## Hvordan utvikle dine egne verktøy

For å utvikle dine egne tilpassede verktøy for Agenten, følg disse retningslinjene:

- Opprett en ny klasse som arver fra `AgentTool`-klassen. Selv om grensesnittet er kompatibelt med LangChain, tilbyr denne eksempelimplementeringen sin egen `AgentTool`-klasse, som du bør arve fra ([kilde](../backend/app/agents/tools/agent_tool.py)).

- Se på eksempelimplementeringen av et [BMI-beregningsverktøy](../examples/agents/tools/bmi/bmi.py). Dette eksempelet viser hvordan du oppretter et verktøy som beregner Body Mass Index (BMI) basert på brukerinput.

  - Navnet og beskrivelsen som er deklarert på verktøyet, brukes når LLM vurderer hvilket verktøy som skal brukes for å svare på brukerens spørsmål. Med andre ord, de er innebygd i prompten når LLM påkalles. Så det anbefales å beskrive så presist som mulig.

- [Valgfritt] Når du har implementert ditt tilpassede verktøy, anbefales det å verifisere funksjonaliteten ved hjelp av testskriptet ([eksempel](../examples/agents/tools/bmi/test_bmi.py)). Dette skriptet vil hjelpe deg med å sikre at verktøyet fungerer som forventet.

- Etter at du har fullført utviklingen og testingen av ditt tilpassede verktøy, flytt implementasjonsfilen til [backend/app/agents/tools/](../backend/app/agents/tools/)-mappen. Åpern deretter [backend/app/agents/utils.py](../backend/app/agents/utils.py) og rediger `get_available_tools` slik at brukeren kan velge det utviklede verktøyet.

- [Valgfritt] Legg til klare navn og beskrivelser for frontend. Dette trinnet er valgfritt, men hvis du ikke gjør dette trinnet, vil verktøyets navn og beskrivelse som er deklarert i verktøyet bli brukt. De er for LLM, ikke for brukeren, så det anbefales å legge til en dedikert forklaring for bedre brukeropplevelse.

  - Rediger i18n-filer. Åpn [en/index.ts](../frontend/src/i18n/en/index.ts) og legg til ditt eget `name` og `description` i `agent.tools`.
  - Rediger også `xx/index.ts`. Der `xx` representerer landkoden du ønsker.

- Kjør `npx cdk deploy` for å distribuere endringene dine. Dette vil gjøre ditt tilpassede verktøy tilgjengelig i den tilpassede bot-skjermen.

## Bidrag

**Bidrag til verktøylageret er velkomne!** Hvis du utvikler et nyttig og godt implementert verktøy, kan du vurdere å bidra med det til prosjektet ved å sende inn en issue eller en pull request.