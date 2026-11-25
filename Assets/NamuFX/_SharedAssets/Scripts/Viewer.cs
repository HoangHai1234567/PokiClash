using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
#if ENABLE_INPUT_SYSTEM && !ENABLE_LEGACY_INPUT_MANAGER
using UnityEngine.InputSystem;
#endif

public class Viewer : MonoBehaviour
{
    public ParticleSystem[] Particles;
    public int showNum = 0;
    public GameObject ShowPos;
    [Header("UI Elements")]
    public Text _fxNameText;
    public Button _PlayButton;
    public Button _PauseButton;
    public Text _PauseText;

    public float Rotspeed;
    public GameObject _Cam;

    private bool isPaused;
   
    // Start is called before the first frame update
    void Start()
    {
        for(int i = 0; i < Particles.Length; i++)
        {
            Particles[i].gameObject.SetActive(false);
        }
        isPaused = false;
        _PauseButton.gameObject.SetActive(false);
        _PlayButton.gameObject.SetActive(true);
    }

    // Update is called once per frame
    void Update()
    {
        showNum = Mathf.Clamp(showNum, 0, Particles.Length - 1);

        if (!isPaused)
        {
            _fxNameText.text = Particles[showNum].gameObject.name;
            _PauseText.text = "Pause";
        }
        else
        {
            _fxNameText.text = Particles[showNum].gameObject.name + "-" + "Paused";
            _PauseText.text = "Resume";
        }

        if (Particles[showNum].IsAlive())
        {
            _PauseButton.gameObject.SetActive(true);
            _PlayButton.gameObject.SetActive(false);
        }
        else
        {
            _PauseButton.gameObject.SetActive(false);
            _PlayButton.gameObject.SetActive(true);
        }



        if(KeyDown(KeyCode.LeftArrow))
        {
            Previous();
        }
        if (KeyDown(KeyCode.RightArrow))
        {
            Next();
        }
        if ((KeyDown(KeyCode.Space) && !Particles[showNum].IsAlive()) || (KeyDown(KeyCode.Space) && isPaused))
        {
            PlayFX();
        }
        else if(KeyDown(KeyCode.Space) && Particles[showNum].IsAlive() && !isPaused)
        {
            PauseFX();
        }

        if(MouseDown0())
        {
            Ray ray = _Cam.GetComponent<Camera>().ScreenPointToRay(MousePos());
            RaycastHit hit;
            if(Physics.Raycast(ray, out hit, Mathf.Infinity))
            {
                GameObject spawnFX = Instantiate(Particles[showNum].gameObject, hit.point, Quaternion.FromToRotation(Particles[showNum].transform.up, hit.normal));
                spawnFX.gameObject.SetActive(true);
                spawnFX.GetComponent<ParticleSystem>().Play();

                Destroy(spawnFX, spawnFX.GetComponent<ParticleSystem>().main.duration);
            }
            
        }
        

        //Camera Rotate
        if (MouseHeld1())
        {
            float xRotateMove = MouseAxis(true) * Time.deltaTime * Rotspeed;
            float yRotateMove = MouseAxis(false) * Time.deltaTime * Rotspeed;

            Vector3 stagePosition = ShowPos.transform.position;

            _Cam.transform.RotateAround(stagePosition, Vector3.up, xRotateMove);
            _Cam.transform.RotateAround(stagePosition, Vector3.right, -yRotateMove);

            _Cam.transform.LookAt(stagePosition);
        }
        

    }

    public void Next()
    {
        isPaused = false;
        if (showNum != Particles.Length - 1)
        {
            Particles[showNum].gameObject.SetActive(false);
            showNum += 1;
            Particles[showNum].gameObject.transform.position = ShowPos.transform.position;
            Particles[showNum].gameObject.SetActive(true);
        }
        else
        {
            Particles[showNum].gameObject.SetActive(false);
            showNum = 0;
            Particles[showNum].gameObject.transform.position = ShowPos.transform.position;
            Particles[showNum].gameObject.SetActive(true);

        }

    }

    public void Previous()
    {
        isPaused = false;
        if (showNum != 0)
        {
            Particles[showNum].gameObject.SetActive(false);
            showNum -= 1;
            Particles[showNum].gameObject.transform.position = ShowPos.transform.position;
            Particles[showNum].gameObject.SetActive(true);
        }
        else
        {
            Particles[showNum].gameObject.SetActive(false);
            showNum = Particles.Length -1;
            Particles[showNum].gameObject.transform.position = ShowPos.transform.position;
            Particles[showNum].gameObject.SetActive(true);
        }
        
    }

    public void PlayFX()
    {
        if (!Particles[showNum].IsAlive())
        {
            Particles[showNum].gameObject.transform.position = ShowPos.transform.position;
            Particles[showNum].gameObject.SetActive(true);
            Particles[showNum].Play();
        }
        if(isPaused)
        {
            Particles[showNum].Play();
            isPaused = false;
        }
    }

    public void PauseFX()
    {
        if (!isPaused)
        {
            isPaused = true;
            Particles[showNum].Pause();
        }
        else if (isPaused)
        {
            isPaused = false;
            Particles[showNum].Play();
        }
    }

    // PokiClash 2026-11-25: project chi bat Input System moi, goi Input cu se nem loi -> boc lai.
#if ENABLE_INPUT_SYSTEM && !ENABLE_LEGACY_INPUT_MANAGER
    static bool KeyDown(KeyCode k)
    {
        var kb = Keyboard.current;
        if (kb == null) return false;
        switch (k)
        {
            case KeyCode.LeftArrow: return kb.leftArrowKey.wasPressedThisFrame;
            case KeyCode.RightArrow: return kb.rightArrowKey.wasPressedThisFrame;
            case KeyCode.Space: return kb.spaceKey.wasPressedThisFrame;
        }
        return false;
    }
    static bool MouseDown0() { return Mouse.current != null && Mouse.current.leftButton.wasPressedThisFrame; }
    static bool MouseHeld1() { return Mouse.current != null && Mouse.current.rightButton.isPressed; }
    static Vector3 MousePos() { return Mouse.current != null ? (Vector3)Mouse.current.position.ReadValue() : Vector3.zero; }
    static float MouseAxis(bool x) { if (Mouse.current == null) return 0; var d = Mouse.current.delta.ReadValue() * 0.1f; return x ? d.x : d.y; }
#else
    static bool KeyDown(KeyCode k) { return Input.GetKeyDown(k); }
    static bool MouseDown0() { return Input.GetMouseButtonDown(0); }
    static bool MouseHeld1() { return Input.GetMouseButton(1); }
    static Vector3 MousePos() { return Input.mousePosition; }
    static float MouseAxis(bool x) { return Input.GetAxis(x ? "Mouse X" : "Mouse Y"); }
#endif
}
